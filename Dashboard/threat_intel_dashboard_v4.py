import streamlit as st
import pandas as pd
import plotly.express as px
from pyairtable import Api
from datetime import datetime
import re
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================================================
# CONFIGURATION
# ============================================================================
def get_secret(key, default=None):
    try:
        return st.secrets.get(key, default)
    except (FileNotFoundError, KeyError):
        return default

AIRTABLE_PAT = get_secret("AIRTABLE_PAT")
NVD_API_KEY = get_secret("NVD_API_KEY")
SLACK_WEBHOOK_URL = get_secret("SLACK_WEBHOOK_URL")
SMTP_HOST = get_secret("SMTP_HOST")
SMTP_PORT = int(get_secret("SMTP_PORT", 587))
SMTP_USER = get_secret("SMTP_USER")
SMTP_PASS = get_secret("SMTP_PASS")
ALERT_TO_EMAIL = get_secret("ALERT_TO_EMAIL")

# Base + table IDs. Override in secrets.toml if they differ.
BASE_ID = get_secret("BASE_ID", "appvjtsGiE98O1MhU")
THREATS_TABLE_ID = get_secret("THREATS_TABLE_ID", "tblhkkgT7prpJdO4i")
OTX_TABLE_ID = get_secret("OTX_TABLE_ID", "tbl1bXDTzv8jiVnQ1")  # AlienVault OTX table

SEVERITY_COLORS = {
    "Critical": "#dc2626", "High": "#ea580c", "Medium": "#ca8a04",
    "Low": "#16a34a", "Informational": "#3b82f6", "N/A": "#6b7280",
}
SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Informational", "N/A"]
SEVERITY_MAPPING = {
    "Critical": "Critical", "High": "High", "Medium": "Medium", "Med": "Medium",
    "Low": "Low", "Informational": "Informational", "Info": "Informational",
    "Unknown": "N/A", "None": "N/A", "N/A": "N/A", "Na": "N/A", "Nan": "N/A", "": "N/A",
}

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)

# ============================================================================
# PAGE SETUP
# ============================================================================
st.set_page_config(page_title="Threat Intel Dashboard", page_icon="🛡️", layout="wide")
st.title("🛡️ Threat Intelligence Triage Dashboard")

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

# ============================================================================
# NORMALIZATION HELPERS
# ============================================================================
def coerce_to_string(val):
    if isinstance(val, list):
        return ", ".join(str(v) for v in val if v is not None) if val else ""
    if pd.isna(val):
        return ""
    return str(val).strip()

def normalize_severity(val):
    s = coerce_to_string(val)
    if not s or s.lower() == "nan":
        return "N/A"
    first = s.split(",")[0].strip().title()
    return SEVERITY_MAPPING.get(first, first)

def parse_cve_field(val):
    """CVE IDs come as a clean comma-separated string in Airtable; also catch any in free text."""
    s = coerce_to_string(val)
    found = set(m.upper() for m in CVE_PATTERN.findall(s))
    return sorted(found)

def parse_list_field(val):
    """IOC fields are stored as JSON arrays or comma strings. Return a clean list."""
    s = coerce_to_string(val)
    if not s:
        return []
    # Try JSON first
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [str(x).strip() for x in parsed if str(x).strip()]
    except (json.JSONDecodeError, ValueError):
        pass
    # Fall back to comma split
    return [x.strip() for x in s.split(",") if x.strip()]

def split_multi(val):
    """Attack Type / Affected Software are comma-separated multi-values."""
    s = coerce_to_string(val)
    if not s or s.lower() in ("nan", "unknown", "n/a", ""):
        return []
    return [x.strip() for x in s.split(",") if x.strip() and x.strip().lower() not in ("unknown", "n/a")]

def parse_date(val):
    return pd.to_datetime(coerce_to_string(val), errors="coerce")

# ============================================================================
# ALERTING
# ============================================================================
def send_slack_alert(message_text, blocks=None):
    if not SLACK_WEBHOOK_URL:
        return False, "Slack webhook not configured"
    try:
        payload = {"text": message_text}
        if blocks:
            payload["blocks"] = blocks
        r = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        return (r.status_code == 200, "Sent" if r.status_code == 200 else f"HTTP {r.status_code}")
    except Exception as e:
        return False, str(e)

def send_email_alert(subject, html_body):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_TO_EMAIL]):
        return False, "SMTP credentials not configured"
    try:
        msg = MIMEMultipart("alternative")
        msg["From"], msg["To"], msg["Subject"] = SMTP_USER, ALERT_TO_EMAIL, subject
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, "Sent"
    except Exception as e:
        return False, str(e)

# ============================================================================
# NVD ENRICHMENT
# ============================================================================
@st.cache_data(ttl=86400, show_spinner=False)
def fetch_nvd_cve(cve_id):
    try:
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
        headers = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
        vulns = r.json().get("vulnerabilities", [])
        if not vulns:
            return None
        vuln = vulns[0]["cve"]
        cvss = sev = vector = None
        metrics = vuln.get("metrics", {})
        for key in ("cvssMetricV31", "cvssMetricV30"):
            if metrics.get(key):
                m = metrics[key][0]["cvssData"]
                cvss, sev, vector = m.get("baseScore"), m.get("baseSeverity"), m.get("vectorString")
                break
        if cvss is None and metrics.get("cvssMetricV2"):
            m = metrics["cvssMetricV2"][0]
            cvss, sev, vector = m["cvssData"].get("baseScore"), m.get("baseSeverity"), m["cvssData"].get("vectorString")
        descs = vuln.get("descriptions", [])
        desc = next((d["value"] for d in descs if d.get("lang") == "en"), "")
        return {"cvss_score": cvss, "severity": sev, "vector": vector,
                "description": desc[:400], "published": vuln.get("published"),
                "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}"}
    except Exception:
        return None

# ============================================================================
# DATA LOADING — maps the REAL Airtable schema into a common shape
# ============================================================================
def standardize(records, source_label):
    """Map a table's records to a normalized dataframe regardless of source schema."""
    rows = []
    for r in records:
        f = r.get("fields", {})

        # Title: "Title" (Threats) or "title" (OTX)
        title = f.get("Title") or f.get("title") or "Untitled"
        # Summary: "Summary" / "AI Summary"
        summary = f.get("Summary") or f.get("AI Summary") or f.get("description") or ""
        # Source: "Source" (Threats) or "source" (OTX)
        src = f.get("Source") or f.get("source") or source_label
        # Date: prefer published/created
        date = (f.get("Published Date") or f.get("created")
                or f.get("Collected Date") or r.get("createdTime"))

        rows.append({
            "Title": coerce_to_string(title) or "Untitled",
            "Summary": coerce_to_string(summary),
            "Source": coerce_to_string(src) or source_label,
            "Source Table": source_label,
            "Severity Level": normalize_severity(f.get("Severity Level")),
            "Relevance Score": pd.to_numeric(f.get("Relevance Score"), errors="coerce"),
            "Attack Types": split_multi(f.get("Attack Type")),
            "Affected Software": split_multi(f.get("Affected Software")),
            "CVEs": parse_cve_field(f.get("CVE IDs")) or parse_cve_field(
                f"{coerce_to_string(title)} {coerce_to_string(summary)}"),
            "Category": coerce_to_string(f.get("Category")) or coerce_to_string(f.get("Source Type")),
            "URL": coerce_to_string(f.get("URL")) or coerce_to_string(f.get("references")),
            "Recommended Actions": coerce_to_string(f.get("Recommended Actions") or f.get("Recommended Action")),
            "Tags": split_multi(f.get("Tags") or f.get("tags")),
            "IOC IPs": parse_list_field(f.get("IOC IPs")),
            "IOC Domains": parse_list_field(f.get("IOC Domains")),
            "IOC URLs": parse_list_field(f.get("IOC URLs")),
            "IOC Hashes": parse_list_field(f.get("IOC Hashes")),
            "_date": parse_date(date),
        })
    return pd.DataFrame(rows)

@st.cache_data(ttl=60)
def load_source(table_id, label):
    if not AIRTABLE_PAT:
        return pd.DataFrame(), "AIRTABLE_PAT not set in secrets"
    if not table_id:
        return pd.DataFrame(), "table id not configured"
    try:
        api = Api(AIRTABLE_PAT)
        records = api.table(BASE_ID, table_id).all()
        return standardize(records, label), None
    except Exception as e:
        return pd.DataFrame(), str(e)

# ============================================================================
# SOURCE SELECTOR
# ============================================================================
col_src, col_refresh, col_time = st.columns([2, 1, 3])
with col_src:
    source_options = ["Threats (Krebs/RSS)"]
    if OTX_TABLE_ID:
        source_options += ["AlienVault OTX", "Combined (both)"]
    source_choice = st.selectbox("Data source", source_options)
with col_refresh:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()
with col_time:
    st.caption(f"Last loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

errors = []
frames = []
if source_choice in ("Threats (Krebs/RSS)", "Combined (both)"):
    d, err = load_source(THREATS_TABLE_ID, "Threats")
    if err: errors.append(f"Threats: {err}")
    else: frames.append(d)
if source_choice in ("AlienVault OTX", "Combined (both)") and OTX_TABLE_ID:
    d, err = load_source(OTX_TABLE_ID, "AlienVault OTX")
    if err: errors.append(f"OTX: {err}")
    else: frames.append(d)

if not OTX_TABLE_ID:
    st.info("💡 AlienVault OTX source not configured (set `OTX_TABLE_ID` in secrets).")

for e in errors:
    st.error(f"Failed to load — {e}")

df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
if df.empty:
    st.warning("No data loaded. Check your PAT, base ID, and table IDs.")
    st.stop()

# ============================================================================
# DATA QUALITY CHECK
# ============================================================================
score_all_zero = (df["Relevance Score"].fillna(0) == 0).all()
sev_all_same = df["Severity Level"].nunique() == 1

if score_all_zero:
    st.warning("⚠️ **Relevance Score is 0 (or empty) for every record.** This field isn't being "
               "populated by your n8n AI step yet. Score-based charts and the average will read 0 "
               "until that's fixed upstream.")
if sev_all_same:
    only = df["Severity Level"].iloc[0]
    st.warning(f"⚠️ **Every record has Severity Level = '{only}'.** Your n8n workflow is assigning the "
               f"same severity to all threats. The dashboard is showing this faithfully — the fix is "
               f"in the AI grading step, not here.")

with st.expander("🔎 Data Quality Check"):
    q = st.columns(5)
    q[0].metric("Total Records", len(df))
    q[1].metric("Severity Filled", f"{(df['Severity Level'] != 'N/A').sum()}/{len(df)}")
    q[2].metric("Score > 0", int((df['Relevance Score'].fillna(0) > 0).sum()))
    q[3].metric("With CVEs", df["CVEs"].apply(bool).sum())
    q[4].metric("With IOCs", df.apply(lambda r: bool(r["IOC IPs"] or r["IOC Domains"]
                                                      or r["IOC URLs"] or r["IOC Hashes"]), axis=1).sum())
    qc1, qc2 = st.columns(2)
    with qc1:
        st.markdown("**Severity values:**")
        st.write(df["Severity Level"].value_counts().to_dict())
    with qc2:
        st.markdown("**By source table:**")
        st.write(df["Source Table"].value_counts().to_dict())

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.header("🔍 Filter Threats")
search_term = st.sidebar.text_input("Search title or summary", "")

severities = [s for s in SEVERITY_ORDER if s in df["Severity Level"].unique()]
selected_severity = st.sidebar.multiselect("Severity Level", severities, default=severities)

sources = sorted(df["Source"].dropna().unique().tolist())
selected_sources = st.sidebar.multiselect("Source", sources, default=sources)

# Attack type filter (flattened)
all_attack_types = sorted({a for lst in df["Attack Types"] for a in lst})
selected_attacks = st.sidebar.multiselect("Attack Type (any of)", all_attack_types, default=[])

valid_scores = df["Relevance Score"].dropna()
if len(valid_scores) and valid_scores.max() > valid_scores.min():
    min_s, max_s = int(valid_scores.min()), int(max(valid_scores.max(), 1))
    score_range = st.sidebar.slider("Relevance Score Range", min_s, max_s, (min_s, max_s))
else:
    score_range = None
    st.sidebar.caption("Relevance Score filter hidden (all scores are 0).")

# Apply filters
filtered_df = df[df["Severity Level"].isin(selected_severity) & df["Source"].isin(selected_sources)]
if selected_attacks:
    filtered_df = filtered_df[filtered_df["Attack Types"].apply(
        lambda lst: any(a in lst for a in selected_attacks))]
if score_range:
    filtered_df = filtered_df[filtered_df["Relevance Score"].fillna(0).between(score_range[0], score_range[1])]
if search_term:
    mask = (filtered_df["Title"].str.contains(search_term, case=False, na=False)
            | filtered_df["Summary"].str.contains(search_term, case=False, na=False))
    filtered_df = filtered_df[mask]

filtered_df = filtered_df.sort_values(by="Relevance Score", ascending=False, na_position="last")

# ============================================================================
# TOP METRICS
# ============================================================================
st.markdown("### Executive Summary")
m = st.columns(6)
total = len(filtered_df)
crit = int((filtered_df["Severity Level"] == "Critical").sum())
high = int((filtered_df["Severity Level"] == "High").sum())
avg_score = filtered_df["Relevance Score"].dropna().mean() if total else 0
unique_cves = len({c for cs in filtered_df["CVEs"] for c in cs})
total_iocs = int(filtered_df.apply(lambda r: len(r["IOC IPs"]) + len(r["IOC Domains"])
                                   + len(r["IOC URLs"]) + len(r["IOC Hashes"]), axis=1).sum())
m[0].metric("Total Threats", total)
m[1].metric("🔴 Critical", crit)
m[2].metric("🟠 High", high)
m[3].metric("Avg Score", f"{(avg_score or 0):.1f}/100")
m[4].metric("Unique CVEs", unique_cves)
m[5].metric("Total IOCs", total_iocs)

st.divider()

# ============================================================================
# TABS
# ============================================================================
tab_analytics, tab_iocs, tab_table, tab_dive, tab_alerts, tab_export = st.tabs(
    ["📊 Analytics", "🎯 IOCs", "📋 Threat Table", "🔬 Deep Dive", "🔔 Alerts", "💾 Export"])

# ----- ANALYTICS -----
with tab_analytics:
    st.markdown("### Threat Landscape")
    if filtered_df.empty:
        st.info("No threats match the current filters.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sev = filtered_df["Severity Level"].value_counts().reset_index()
            sev.columns = ["Severity", "Count"]
            fig = px.pie(sev, values="Count", names="Severity", hole=0.5,
                         title="Severity Distribution", color="Severity",
                         color_discrete_map=SEVERITY_COLORS,
                         category_orders={"Severity": SEVERITY_ORDER})
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            # Attack Type frequency (real field, was unused before)
            atk = [a for lst in filtered_df["Attack Types"] for a in lst]
            if atk:
                ac = pd.Series(atk).value_counts().reset_index()
                ac.columns = ["Attack Type", "Count"]
                fig = px.bar(ac, x="Count", y="Attack Type", orientation="h",
                             title="Attack Types", color="Count", color_continuous_scale="Reds")
                fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No Attack Type data.")

        c3, c4 = st.columns(2)
        with c3:
            # Source breakdown
            sc = filtered_df["Source"].value_counts().reset_index()
            sc.columns = ["Source", "Count"]
            fig = px.bar(sc, x="Source", y="Count", title="Threats by Source",
                         color="Count", color_continuous_scale="Blues", text="Count")
            fig.update_traces(textposition="outside")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with c4:
            sw = [s for lst in filtered_df["Affected Software"] for s in lst]
            if sw:
                wc = pd.Series(sw).value_counts().head(10).reset_index()
                wc.columns = ["Software", "Mentions"]
                fig = px.bar(wc, x="Mentions", y="Software", orientation="h",
                             title="Top 10 Affected Software", color="Mentions",
                             color_continuous_scale="Oranges")
                fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No Affected Software data.")

        # Score histogram only if scores are meaningful
        if (filtered_df["Relevance Score"].fillna(0) > 0).any():
            fig = px.histogram(filtered_df, x="Relevance Score", nbins=20,
                               title="Relevance Score Distribution",
                               color_discrete_sequence=["#3b82f6"])
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("📉 Relevance Score histogram hidden — all scores are currently 0.")

        # Timeline if dates parse
        if filtered_df["_date"].notna().sum() >= 2:
            tdf = filtered_df.dropna(subset=["_date"]).copy()
            tdf["Day"] = tdf["_date"].dt.date
            daily = tdf.groupby(["Day", "Severity Level"]).size().reset_index(name="Count")
            fig = px.bar(daily, x="Day", y="Count", color="Severity Level",
                         color_discrete_map=SEVERITY_COLORS, title="Threats Over Time",
                         category_orders={"Severity Level": SEVERITY_ORDER})
            fig.update_layout(barmode="stack")
            st.plotly_chart(fig, use_container_width=True)

# ----- IOCs -----
with tab_iocs:
    st.markdown("### Indicators of Compromise")
    st.caption("Extracted from the IOC fields your n8n workflow populates.")
    ips = [x for lst in filtered_df["IOC IPs"] for x in lst]
    domains = [x for lst in filtered_df["IOC Domains"] for x in lst]
    urls = [x for lst in filtered_df["IOC URLs"] for x in lst]
    hashes = [x for lst in filtered_df["IOC Hashes"] for x in lst]

    ic = st.columns(4)
    ic[0].metric("IPs", len(ips))
    ic[1].metric("Domains", len(domains))
    ic[2].metric("URLs", len(urls))
    ic[3].metric("Hashes", len(hashes))

    if not any([ips, domains, urls, hashes]):
        st.info("No IOCs in the current selection.")
    else:
        ioc_type = st.radio("IOC type", ["IPs", "Domains", "URLs", "Hashes"], horizontal=True)
        chosen = {"IPs": ips, "Domains": domains, "URLs": urls, "Hashes": hashes}[ioc_type]
        if chosen:
            counts = pd.Series(chosen).value_counts().reset_index()
            counts.columns = [ioc_type, "Occurrences"]
            st.dataframe(counts, use_container_width=True, hide_index=True, height=400)
            st.download_button(f"📥 Export {ioc_type} (one per line)",
                               data="\n".join(dict.fromkeys(chosen)),
                               file_name=f"iocs_{ioc_type.lower()}_{datetime.now():%Y%m%d}.txt",
                               mime="text/plain")
        else:
            st.info(f"No {ioc_type} in the current selection.")

# ----- THREAT TABLE -----
with tab_table:
    st.markdown("### Actionable Threats")
    st.caption(f"Showing {len(filtered_df)} threats")
    t = filtered_df.copy()
    t["CVE IDs"] = t["CVEs"].apply(lambda x: ", ".join(x[:4]) if x else "—")
    t["Attack Type"] = t["Attack Types"].apply(lambda x: ", ".join(x[:3]) if x else "—")
    cols = ["Title", "Source", "Severity Level", "Relevance Score", "Attack Type", "CVE IDs"]
    disp = t[cols].copy()

    def color_sev(v):
        return f"background-color: {SEVERITY_COLORS.get(str(v), '#6b7280')}; color: white; font-weight: bold; text-align: center;"
    def color_score(v):
        try: x = float(v)
        except (TypeError, ValueError): return ""
        if x >= 80: return "background-color: #dc2626; color: white;"
        if x >= 60: return "background-color: #ea580c; color: white;"
        if x >= 40: return "background-color: #ca8a04; color: white;"
        if x > 0:  return "background-color: #16a34a; color: white;"
        return "color: #9ca3af;"

    def apply_style(s, fn, col):
        return s.map(fn, subset=[col]) if hasattr(s, "map") else s.applymap(fn, subset=[col])
    styled = disp.style
    styled = apply_style(styled, color_sev, "Severity Level")
    styled = apply_style(styled, color_score, "Relevance Score")
    styled = styled.format({"Relevance Score": lambda v: f"{v:.0f}" if pd.notna(v) else "—"})
    st.dataframe(styled, use_container_width=True, hide_index=True, height=520)

# ----- DEEP DIVE -----
with tab_dive:
    st.markdown("### Threat Deep Dive")
    titles = filtered_df["Title"].dropna().unique().tolist()
    if not titles:
        st.info("No threats match the current filters.")
    else:
        sel = st.selectbox("Select a Threat", titles)
        d = filtered_df[filtered_df["Title"] == sel].iloc[0]
        sev = d["Severity Level"]
        score = d["Relevance Score"]

        b = st.columns(3)
        b[0].markdown(f"<div style='background:{SEVERITY_COLORS.get(sev, '#6b7280')};padding:1rem;"
                      f"border-radius:8px;text-align:center;color:white;'><strong>Severity</strong>"
                      f"<br/>{sev}</div>", unsafe_allow_html=True)
        b[1].markdown(f"<div style='background:#1f2937;padding:1rem;border-radius:8px;text-align:center;"
                      f"color:white;'><strong>Relevance Score</strong><br/>"
                      f"{f'{score:.0f} / 100' if pd.notna(score) and score > 0 else 'Not scored'}</div>",
                      unsafe_allow_html=True)
        b[2].markdown(f"<div style='background:#374151;padding:1rem;border-radius:8px;text-align:center;"
                      f"color:white;'><strong>Source</strong><br/>{d['Source']}</div>",
                      unsafe_allow_html=True)

        st.markdown("")
        if d["Attack Types"]:
            st.markdown("**Attack Types:** " + ", ".join(d["Attack Types"]))
        if d["Affected Software"]:
            st.info(f"**Affected Software:** {', '.join(d['Affected Software'])}")
        st.markdown("#### Summary")
        st.write(d["Summary"] or "No summary available.")
        if d["URL"]:
            st.markdown(f"[🔗 Original source]({d['URL'].split(',')[0].strip()})")
        if d["Recommended Actions"]:
            st.markdown("#### Recommended Actions")
            st.write(d["Recommended Actions"])

        # IOCs for this threat
        threat_iocs = {"IPs": d["IOC IPs"], "Domains": d["IOC Domains"],
                       "URLs": d["IOC URLs"], "Hashes": d["IOC Hashes"]}
        if any(threat_iocs.values()):
            st.markdown("#### Indicators of Compromise")
            for k, v in threat_iocs.items():
                if v:
                    with st.expander(f"{k} ({len(v)})"):
                        st.code("\n".join(v[:50]))

        # CVE enrichment from the real CVE IDs field
        if d["CVEs"]:
            st.markdown("#### CVE Enrichment (NVD)")
            for cve in d["CVEs"][:5]:
                with st.expander(f"📌 {cve}"):
                    info = fetch_nvd_cve(cve)
                    if not info:
                        st.warning(f"Could not retrieve {cve}.")
                        continue
                    cc = st.columns(3)
                    cvss = info.get("cvss_score")
                    nvd_sev = (info.get("severity") or "Unknown")
                    color = SEVERITY_COLORS.get(nvd_sev.title(), "#6b7280")
                    cc[0].markdown(f"<div style='background:{color};padding:.75rem;border-radius:6px;"
                                   f"text-align:center;color:white;'><strong>CVSS</strong><br/>{cvss or '—'}</div>",
                                   unsafe_allow_html=True)
                    cc[1].markdown(f"<div style='background:{color};padding:.75rem;border-radius:6px;"
                                   f"text-align:center;color:white;'><strong>NVD Severity</strong><br/>{nvd_sev}</div>",
                                   unsafe_allow_html=True)
                    cc[2].markdown(f"<div style='background:#1f2937;padding:.75rem;border-radius:6px;"
                                   f"text-align:center;color:white;'><strong>Published</strong><br/>"
                                   f"{(info.get('published') or '')[:10] or '—'}</div>", unsafe_allow_html=True)
                    if info.get("vector"): st.caption(f"Vector: `{info['vector']}`")
                    if info.get("description"): st.write(info["description"])
                    st.markdown(f"[View on NVD →]({info['link']})")

        # Per-threat alert
        st.markdown("#### Send Alert")
        a = st.columns(2)
        with a[0]:
            if st.button("💬 Send to Slack", key="dive_slack"):
                ok, msg = send_slack_alert(f"🚨 {sev} threat: {sel}")
                st.success("Sent") if ok else st.error(f"Failed: {msg}")
                if ok: st.session_state.alert_log.append({"time": datetime.now(), "channel": "Slack", "target": sel})
        with a[1]:
            if st.button("📧 Send to Email", key="dive_email"):
                html = f"<h3>{sel}</h3><p>Severity: {sev}</p><p>{d['Summary'][:500]}</p>"
                ok, msg = send_email_alert(f"Threat Alert: {sel[:60]}", html)
                st.success("Sent") if ok else st.error(f"Failed: {msg}")
                if ok: st.session_state.alert_log.append({"time": datetime.now(), "channel": "Email", "target": sel})

# ----- ALERTS -----
with tab_alerts:
    st.markdown("### Alert Configuration & Dispatch")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Slack")
        st.success("✅ Slack webhook configured") if SLACK_WEBHOOK_URL else st.warning("⚠️ No Slack webhook in secrets")
        if st.button("📨 Send Slack Test"):
            ok, msg = send_slack_alert("✅ Threat Intel Dashboard test alert.")
            st.success("Test sent") if ok else st.error(f"Failed: {msg}")
    with c2:
        st.markdown("#### Email (SMTP)")
        ready = all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_TO_EMAIL])
        st.success(f"✅ SMTP configured → {ALERT_TO_EMAIL}") if ready else st.warning("⚠️ SMTP incomplete")
        if st.button("📨 Send Email Test"):
            ok, msg = send_email_alert("Dashboard Test", "<p>✅ Connection verified.</p>")
            st.success("Test sent") if ok else st.error(f"Failed: {msg}")

    st.divider()
    crit_df = filtered_df[filtered_df["Severity Level"] == "Critical"]
    high_df = filtered_df[filtered_df["Severity Level"].isin(["Critical", "High"])]
    st.caption(f"{len(crit_df)} Critical / {len(high_df)} Critical+High in current filter.")
    bc = st.columns(2)
    with bc[0]:
        if st.button(f"💬 Slack all Critical ({len(crit_df)})"):
            sent = sum(send_slack_alert(f"🚨 Critical: {t['Title']}")[0] for _, t in crit_df.iterrows())
            st.success(f"Sent {sent}")
    with bc[1]:
        if st.button(f"💬 Slack Critical+High ({len(high_df)})"):
            sent = sum(send_slack_alert(f"🚨 {t['Severity Level']}: {t['Title']}")[0] for _, t in high_df.iterrows())
            st.success(f"Sent {sent}")

    st.divider()
    st.markdown("#### Alert Log (this session)")
    if st.session_state.alert_log:
        log = pd.DataFrame(st.session_state.alert_log)
        log["time"] = log["time"].astype(str)
        st.dataframe(log.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.caption("No alerts sent yet.")

# ----- EXPORT -----
with tab_export:
    st.markdown("### Export Filtered Data")
    st.write(f"Export {len(filtered_df)} filtered threats")
    exp = filtered_df.copy()
    for c in ["Attack Types", "Affected Software", "CVEs", "Tags",
              "IOC IPs", "IOC Domains", "IOC URLs", "IOC Hashes"]:
        exp[c] = exp[c].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
    exp = exp.drop(columns=["_date"], errors="ignore")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button("📥 Download CSV", data=exp.to_csv(index=False),
                       file_name=f"threat_intel_{stamp}.csv", mime="text/csv")
    st.download_button("📥 Download JSON", data=exp.to_json(orient="records", indent=2),
                       file_name=f"threat_intel_{stamp}.json", mime="application/json")
