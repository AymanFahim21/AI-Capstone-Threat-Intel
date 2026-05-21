import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyairtable import Api
from datetime import datetime, timedelta
import re
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

BASE_ID = "appvjtsGiE98O1MhU"
TABLE_ID = "tblhkkgT7prpJdO4i"

SEVERITY_COLORS = {
    "Critical": "#dc2626", "High": "#ea580c", "Medium": "#ca8a04",
    "Low": "#16a34a", "Informational": "#3b82f6", "N/A": "#6b7280",
}
PRIORITY_COLORS = {
    "Critical": "#dc2626", "High": "#ea580c", "Medium": "#ca8a04",
    "Low": "#16a34a", "N/A": "#6b7280",
}
SEVERITY_ORDER = ["Critical", "High", "Medium", "Low", "Informational", "N/A"]
PRIORITY_ORDER = ["Critical", "High", "Medium", "Low", "N/A"]

# Normalize anything Airtable throws at us
SEVERITY_MAPPING = {
    "Critical": "Critical", "High": "High", "Medium": "Medium", "Med": "Medium",
    "Low": "Low", "Informational": "Informational", "Info": "Informational",
    "Unknown": "N/A", "None": "N/A", "N/A": "N/A", "Na": "N/A", "Nan": "N/A",
}
PRIORITY_MAPPING = {
    "Critical": "Critical", "High": "High", "Medium": "Medium", "Med": "Medium",
    "Low": "Low", "Unknown": "N/A", "None": "N/A", "N/A": "N/A", "Na": "N/A", "Nan": "N/A",
}

CVE_PATTERN = re.compile(r"CVE-\d{4}-\d{4,7}", re.IGNORECASE)
MITRE_PATTERN = re.compile(r"\bT\d{4}(?:\.\d{3})?\b")

MITRE_TECHNIQUES = {
    "T1003": "OS Credential Dumping", "T1005": "Data from Local System",
    "T1021": "Remote Services", "T1027": "Obfuscated Files or Information",
    "T1036": "Masquerading", "T1041": "Exfiltration Over C2 Channel",
    "T1047": "Windows Management Instrumentation", "T1053": "Scheduled Task/Job",
    "T1055": "Process Injection", "T1057": "Process Discovery",
    "T1059": "Command and Scripting Interpreter", "T1068": "Exploitation for Privilege Escalation",
    "T1071": "Application Layer Protocol", "T1078": "Valid Accounts",
    "T1082": "System Information Discovery", "T1083": "File and Directory Discovery",
    "T1090": "Proxy", "T1095": "Non-Application Layer Protocol",
    "T1098": "Account Manipulation", "T1105": "Ingress Tool Transfer",
    "T1110": "Brute Force", "T1112": "Modify Registry",
    "T1133": "External Remote Services", "T1140": "Deobfuscate/Decode Files",
    "T1190": "Exploit Public-Facing Application", "T1203": "Exploitation for Client Execution",
    "T1204": "User Execution", "T1210": "Exploitation of Remote Services",
    "T1218": "System Binary Proxy Execution", "T1219": "Remote Access Software",
    "T1486": "Data Encrypted for Impact", "T1490": "Inhibit System Recovery",
    "T1496": "Resource Hijacking", "T1497": "Virtualization/Sandbox Evasion",
    "T1505": "Server Software Component", "T1518": "Software Discovery",
    "T1543": "Create or Modify System Process", "T1547": "Boot or Logon Autostart Execution",
    "T1548": "Abuse Elevation Control Mechanism", "T1552": "Unsecured Credentials",
    "T1555": "Credentials from Password Stores", "T1556": "Modify Authentication Process",
    "T1557": "Adversary-in-the-Middle", "T1562": "Impair Defenses",
    "T1564": "Hide Artifacts", "T1566": "Phishing",
    "T1567": "Exfiltration Over Web Service", "T1569": "System Services",
    "T1570": "Lateral Tool Transfer", "T1571": "Non-Standard Port",
    "T1572": "Protocol Tunneling", "T1573": "Encrypted Channel",
    "T1574": "Hijack Execution Flow", "T1583": "Acquire Infrastructure",
    "T1584": "Compromise Infrastructure", "T1588": "Obtain Capabilities",
    "T1595": "Active Scanning", "T1608": "Stage Capabilities",
}

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
    """Airtable returns multi-selects as lists. Flatten everything to a single string."""
    if pd.isna(val) if not isinstance(val, list) else False:
        return ""
    if isinstance(val, list):
        return ", ".join(str(v) for v in val if v is not None) if val else ""
    return str(val).strip()

def normalize_categorical(val, mapping):
    """Handle list/string/NaN, title-case, then map variants to canonical form."""
    s = coerce_to_string(val)
    if not s or s.lower() == "nan":
        return "N/A"
    # If it's a list joined with commas, take the first non-empty token
    first = s.split(",")[0].strip()
    if not first:
        return "N/A"
    normalized = first.title()
    return mapping.get(normalized, normalized)

def extract_cves(text):
    if pd.isna(text):
        return []
    return sorted(set(m.upper() for m in CVE_PATTERN.findall(str(text))))

def extract_mitre(text):
    if pd.isna(text):
        return []
    return sorted(set(m.upper() for m in MITRE_PATTERN.findall(str(text))))

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
        data = r.json()
        vulns = data.get("vulnerabilities", [])
        if not vulns:
            return None
        vuln = vulns[0]["cve"]
        cvss_score = severity = vector = None
        metrics = vuln.get("metrics", {})
        for key in ("cvssMetricV31", "cvssMetricV30"):
            if key in metrics and metrics[key]:
                m = metrics[key][0]["cvssData"]
                cvss_score = m.get("baseScore")
                severity = m.get("baseSeverity")
                vector = m.get("vectorString")
                break
        if cvss_score is None and "cvssMetricV2" in metrics and metrics["cvssMetricV2"]:
            m = metrics["cvssMetricV2"][0]
            cvss_score = m["cvssData"].get("baseScore")
            severity = m.get("baseSeverity")
            vector = m["cvssData"].get("vectorString")
        descs = vuln.get("descriptions", [])
        description = next((d["value"] for d in descs if d.get("lang") == "en"), "")
        return {
            "cve_id": cve_id, "cvss_score": cvss_score, "severity": severity,
            "vector": vector, "description": description[:400],
            "published": vuln.get("published"),
            "link": f"https://nvd.nist.gov/vuln/detail/{cve_id}",
        }
    except Exception:
        return None

# ============================================================================
# ALERTING
# ============================================================================
def send_slack_alert(message_text, blocks=None):
    if not SLACK_WEBHOOK_URL:
        return False, "Slack webhook not configured"
    try:
        payload = {"text": message_text}
        if blocks: payload["blocks"] = blocks
        r = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        return (r.status_code == 200, "Sent" if r.status_code == 200 else f"HTTP {r.status_code}")
    except Exception as e:
        return False, str(e)

def send_email_alert(subject, html_body):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_TO_EMAIL]):
        return False, "SMTP credentials not configured"
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_USER
        msg["To"] = ALERT_TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, "Sent"
    except Exception as e:
        return False, str(e)

def build_slack_blocks_for_threat(threat):
    combined = str(threat.get("Title", "")) + " " + str(threat.get("Summary", ""))
    cves = extract_cves(combined)
    return [
        {"type": "header", "text": {"type": "plain_text", "text": f"🚨 {threat.get('Priority Ranking', 'Unknown')} Threat"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*{threat.get('Title', 'Untitled')}*"}},
        {"type": "section", "fields": [
            {"type": "mrkdwn", "text": f"*Severity:* {threat.get('Severity Level', 'N/A')}"},
            {"type": "mrkdwn", "text": f"*Score:* {float(threat.get('Relevance Score', 0)):.0f}/100"},
            {"type": "mrkdwn", "text": f"*Affected:* {str(threat.get('Affected Software', 'Unknown'))[:80]}"},
            {"type": "mrkdwn", "text": f"*CVEs:* {', '.join(cves[:3]) if cves else 'None detected'}"},
        ]},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"_{str(threat.get('Summary', ''))[:500]}_"}},
    ]

def build_email_html_for_threats(threats_df):
    rows = ""
    for _, t in threats_df.iterrows():
        sev_color = SEVERITY_COLORS.get(t.get("Severity Level", "N/A"), "#6b7280")
        cves = extract_cves(str(t.get("Title", "")) + " " + str(t.get("Summary", "")))
        rows += f"""
        <tr>
          <td style="padding:8px;border:1px solid #ddd;"><strong>{t.get('Title', 'Untitled')}</strong></td>
          <td style="padding:8px;border:1px solid #ddd;background:{sev_color};color:white;text-align:center;">{t.get('Severity Level', 'N/A')}</td>
          <td style="padding:8px;border:1px solid #ddd;text-align:center;">{float(t.get('Relevance Score', 0)):.0f}</td>
          <td style="padding:8px;border:1px solid #ddd;">{', '.join(cves[:3]) if cves else '—'}</td>
        </tr>"""
    return f"""<html><body style="font-family:Arial,sans-serif;">
      <h2 style="color:#dc2626;">🚨 Threat Intel Alert — {len(threats_df)} Threats</h2>
      <p>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
      <table style="border-collapse:collapse;width:100%;">
        <tr style="background:#1f2937;color:white;">
          <th style="padding:8px;border:1px solid #ddd;text-align:left;">Title</th>
          <th style="padding:8px;border:1px solid #ddd;">Severity</th>
          <th style="padding:8px;border:1px solid #ddd;">Score</th>
          <th style="padding:8px;border:1px solid #ddd;">CVEs</th>
        </tr>{rows}</table>
      <p style="color:#666;font-size:12px;margin-top:20px;">Sent from Threat Intel Dashboard</p>
    </body></html>"""

# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data(ttl=60)
def load_data():
    if not AIRTABLE_PAT:
        st.error("AIRTABLE_PAT not found in .streamlit/secrets.toml")
        return pd.DataFrame()
    try:
        api = Api(AIRTABLE_PAT)
        table = api.table(BASE_ID, TABLE_ID)
        records = table.all()
        data = []
        for r in records:
            fields = r.get("fields", {})
            fields["_createdTime"] = r.get("createdTime", None)
            data.append(fields)
        df = pd.DataFrame(data)
        expected_cols = ["Title", "Relevance Score", "Priority Ranking",
                         "Severity Level", "Affected Software", "Summary"]
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        # Normalize string fields (handle lists from multi-select, fill NaN)
        df["Title"] = df["Title"].apply(coerce_to_string).replace("", "Untitled")
        df["Summary"] = df["Summary"].apply(coerce_to_string)
        df["Affected Software"] = df["Affected Software"].apply(coerce_to_string).replace("", "Unknown")

        # Normalize categorical fields (case-insensitive, mapping variants)
        df["Severity Level"] = df["Severity Level"].apply(lambda v: normalize_categorical(v, SEVERITY_MAPPING))
        df["Priority Ranking"] = df["Priority Ranking"].apply(lambda v: normalize_categorical(v, PRIORITY_MAPPING))

        # Numeric
        df["Relevance Score"] = pd.to_numeric(df["Relevance Score"], errors="coerce").fillna(0)

        # Timestamp
        if "_createdTime" in df.columns:
            df["_createdTime"] = pd.to_datetime(df["_createdTime"], errors="coerce", utc=True)

        # Pre-extract CVEs and MITRE
        combined = df["Title"].astype(str) + " " + df["Summary"].astype(str)
        df["_cves"] = combined.apply(extract_cves)
        df["_mitre"] = combined.apply(extract_mitre)

        # If Priority Ranking is mostly empty, fall back to Severity Level for triage
        priority_empty_pct = (df["Priority Ranking"] == "N/A").mean()
        df["_priority_effective"] = df["Priority Ranking"]
        df["_priority_fallback_used"] = False
        if priority_empty_pct > 0.8:
            df["_priority_effective"] = df.apply(
                lambda row: row["Severity Level"] if row["Priority Ranking"] == "N/A" else row["Priority Ranking"],
                axis=1
            )
            df["_priority_fallback_used"] = True

        return df
    except Exception as e:
        st.error(f"Failed to connect to Airtable. Check your PAT. Error: {e}")
        return pd.DataFrame()

# ============================================================================
# HEADER
# ============================================================================
col_refresh, col_time = st.columns([1, 5])
with col_refresh:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
df = load_data()
with col_time:
    st.caption(f"Last loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if df.empty:
    st.warning("No data found. Make sure your Airtable table has records!")
    st.stop()

# Pipeline-quality banner
if df["_priority_fallback_used"].any():
    st.warning(
        "⚠️ **Priority Ranking is mostly empty in Airtable.** "
        "Falling back to **Severity Level** for priority-based views. "
        "Fix this upstream in your n8n workflow so the AI step populates 'Priority Ranking' for every record."
    )

# Data quality expander
with st.expander("🔎 Data Quality Check"):
    qc_cols = st.columns(4)
    qc_cols[0].metric("Total Records", len(df))
    qc_cols[1].metric("Severity Filled", f"{(df['Severity Level'] != 'N/A').sum()}/{len(df)}")
    qc_cols[2].metric("Priority Filled", f"{(df['Priority Ranking'] != 'N/A').sum()}/{len(df)}")
    qc_cols[3].metric("With CVEs", df["_cves"].apply(bool).sum())

    qc_left, qc_right = st.columns(2)
    with qc_left:
        st.markdown("**Severity values in data:**")
        st.write(df["Severity Level"].value_counts().to_dict())
    with qc_right:
        st.markdown("**Priority values in data:**")
        st.write(df["Priority Ranking"].value_counts().to_dict())

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================
st.sidebar.header("🔍 Filter Threats")
search_term = st.sidebar.text_input("Search title or summary", "")

priorities = [p for p in PRIORITY_ORDER if p in df["_priority_effective"].unique()]
selected_priority = st.sidebar.multiselect("Priority", priorities, default=priorities)

severities = [s for s in SEVERITY_ORDER if s in df["Severity Level"].unique()]
selected_severity = st.sidebar.multiselect("Severity Level", severities, default=severities)

min_s, max_s = int(df["Relevance Score"].min()), int(df["Relevance Score"].max())
if max_s == min_s:
    max_s = min_s + 1
score_range = st.sidebar.slider("Relevance Score Range", min_s, max_s, (min_s, max_s))

filtered_df = df[
    df["_priority_effective"].isin(selected_priority)
    & df["Severity Level"].isin(selected_severity)
    & df["Relevance Score"].between(score_range[0], score_range[1])
]
if search_term:
    mask = (
        filtered_df["Title"].astype(str).str.contains(search_term, case=False, na=False)
        | filtered_df["Summary"].astype(str).str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[mask]
filtered_df = filtered_df.sort_values(by="Relevance Score", ascending=False)

# ============================================================================
# TOP METRICS
# ============================================================================
st.markdown("### Executive Summary")
m1, m2, m3, m4, m5, m6 = st.columns(6)

total = len(filtered_df)
critical = len(filtered_df[filtered_df["_priority_effective"] == "Critical"])
high = len(filtered_df[filtered_df["_priority_effective"] == "High"])
avg_score = filtered_df["Relevance Score"].mean() if total > 0 else 0
unique_cves = len({c for cs in filtered_df["_cves"] for c in cs})

new_24h = 0
if filtered_df["_createdTime"].notna().any():
    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=1)
    new_24h = int((filtered_df["_createdTime"] > cutoff).sum())

m1.metric("Total Threats", total)
m2.metric("🔴 Critical", critical)
m3.metric("🟠 High", high)
m4.metric("Avg Score", f"{avg_score:.1f}/100")
m5.metric("🆕 New (24h)", new_24h)
m6.metric("Unique CVEs", unique_cves)

st.divider()

# ============================================================================
# TABS
# ============================================================================
tab_analytics, tab_trends, tab_mitre, tab_table, tab_dive, tab_alerts, tab_export = st.tabs(
    ["📊 Analytics", "📈 Trends", "⚔️ MITRE ATT&CK", "📋 Threat Table",
     "🔬 Deep Dive", "🔔 Alerts", "💾 Export"]
)

# ----- ANALYTICS -----
with tab_analytics:
    st.markdown("### Threat Landscape")
    if filtered_df.empty:
        st.info("No threats match the current filters.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            sev_counts = filtered_df["Severity Level"].value_counts().reset_index()
            sev_counts.columns = ["Severity", "Count"]
            sev_counts["Severity"] = pd.Categorical(sev_counts["Severity"], categories=SEVERITY_ORDER, ordered=True)
            sev_counts = sev_counts.sort_values("Severity")
            fig_sev = px.pie(sev_counts, values="Count", names="Severity",
                             title="Severity Distribution", hole=0.5,
                             color="Severity", color_discrete_map=SEVERITY_COLORS,
                             category_orders={"Severity": SEVERITY_ORDER})
            fig_sev.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_sev, use_container_width=True)

        with c2:
            pri_title = "Priority Distribution"
            if df["_priority_fallback_used"].any():
                pri_title += " (using Severity as fallback)"
            pri_counts = filtered_df["_priority_effective"].value_counts().reset_index()
            pri_counts.columns = ["Priority", "Count"]
            pri_counts["Priority"] = pd.Categorical(pri_counts["Priority"], categories=PRIORITY_ORDER, ordered=True)
            pri_counts = pri_counts.sort_values("Priority")
            fig_pri = px.bar(pri_counts, x="Priority", y="Count", title=pri_title,
                             color="Priority", color_discrete_map=PRIORITY_COLORS, text="Count",
                             category_orders={"Priority": PRIORITY_ORDER})
            fig_pri.update_traces(textposition="outside")
            fig_pri.update_layout(showlegend=False)
            st.plotly_chart(fig_pri, use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            fig_hist = px.histogram(filtered_df, x="Relevance Score", nbins=20,
                                    title="Relevance Score Distribution",
                                    color_discrete_sequence=["#3b82f6"])
            fig_hist.update_layout(bargap=0.1)
            st.plotly_chart(fig_hist, use_container_width=True)

        with c4:
            software_list = []
            for s in filtered_df["Affected Software"].astype(str):
                for item in s.split(","):
                    item = item.strip()
                    if item and item.lower() not in ("unknown", "n/a", "nan", ""):
                        software_list.append(item)
            if software_list:
                sw_counts = pd.Series(software_list).value_counts().head(10).reset_index()
                sw_counts.columns = ["Software", "Mentions"]
                fig_sw = px.bar(sw_counts, x="Mentions", y="Software", orientation="h",
                                title="Top 10 Affected Software",
                                color="Mentions", color_continuous_scale="Reds")
                fig_sw.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig_sw, use_container_width=True)
            else:
                st.info("No affected software data available.")

        st.markdown("#### Priority × Severity Heatmap")
        heat = filtered_df.groupby(["_priority_effective", "Severity Level"]).size().reset_index(name="Count")
        if not heat.empty:
            pivot = heat.pivot(index="_priority_effective", columns="Severity Level", values="Count").fillna(0)
            pivot = pivot.reindex([p for p in PRIORITY_ORDER if p in pivot.index])
            pivot = pivot[[s for s in SEVERITY_ORDER if s in pivot.columns]]
            fig_heat = px.imshow(pivot,
                                 labels=dict(x="Severity Level", y="Priority", color="Count"),
                                 color_continuous_scale="Reds", text_auto=True, aspect="auto")
            st.plotly_chart(fig_heat, use_container_width=True)

        st.markdown("#### AI Relevance Score vs NVD CVSS Score")
        st.caption("Validates how well the AI's relevance scoring aligns with the authoritative CVSS rating.")
        if st.button("🔍 Run CVE enrichment on filtered threats"):
            comparison_rows = []
            cve_threats = filtered_df[filtered_df["_cves"].apply(len) > 0]
            if cve_threats.empty:
                st.info("No CVEs detected in the filtered threats.")
            else:
                progress = st.progress(0.0, text="Querying NVD...")
                total_t = len(cve_threats)
                for i, (_, row) in enumerate(cve_threats.iterrows()):
                    for cve in row["_cves"][:3]:
                        info = fetch_nvd_cve(cve)
                        if info and info.get("cvss_score") is not None:
                            comparison_rows.append({
                                "Title": row["Title"][:50], "CVE": cve,
                                "AI Relevance Score": row["Relevance Score"],
                                "CVSS Score": info["cvss_score"] * 10,
                                "CVSS Severity": info["severity"],
                            })
                    progress.progress((i + 1) / total_t, text=f"Querying NVD... {i+1}/{total_t}")
                progress.empty()
                if comparison_rows:
                    comp_df = pd.DataFrame(comparison_rows)
                    fig_scatter = px.scatter(
                        comp_df, x="AI Relevance Score", y="CVSS Score",
                        color="CVSS Severity", hover_data=["Title", "CVE"],
                        title=f"AI vs CVSS — {len(comp_df)} CVE Matches",
                        color_discrete_map={"CRITICAL": "#dc2626", "HIGH": "#ea580c",
                                            "MEDIUM": "#ca8a04", "LOW": "#16a34a"})
                    fig_scatter.add_shape(type="line", x0=0, y0=0, x1=100, y1=100,
                                          line=dict(color="gray", dash="dash"))
                    fig_scatter.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100])
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    st.dataframe(comp_df, use_container_width=True, hide_index=True)
                else:
                    st.warning("No CVSS data returned from NVD.")

# ----- TRENDS -----
with tab_trends:
    st.markdown("### Threat Trends Over Time")
    if filtered_df["_createdTime"].notna().sum() < 2:
        st.info("Not enough timestamp data to chart trends.")
    else:
        days = st.selectbox("Time window", [7, 14, 30, 60, 90], index=2)
        cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)
        trend_df = filtered_df[filtered_df["_createdTime"] >= cutoff].copy()
        trend_df["Date"] = trend_df["_createdTime"].dt.tz_convert(None).dt.date

        if trend_df.empty:
            st.info(f"No threats in the last {days} days.")
        else:
            daily = trend_df.groupby(["Date", "Severity Level"]).size().reset_index(name="Count")
            fig_daily = px.bar(daily, x="Date", y="Count", color="Severity Level",
                               color_discrete_map=SEVERITY_COLORS,
                               category_orders={"Severity Level": SEVERITY_ORDER},
                               title=f"Threats per Day (Last {days} Days)")
            fig_daily.update_layout(barmode="stack")
            st.plotly_chart(fig_daily, use_container_width=True)

            c1, c2 = st.columns(2)
            with c1:
                cum = trend_df.sort_values("_createdTime").reset_index(drop=True)
                cum["Running Total"] = range(1, len(cum) + 1)
                fig_cum = px.line(cum, x="_createdTime", y="Running Total",
                                  title="Cumulative Threat Count", markers=True)
                fig_cum.update_traces(line_color="#3b82f6")
                st.plotly_chart(fig_cum, use_container_width=True)
            with c2:
                avg_daily = trend_df.groupby("Date")["Relevance Score"].mean().reset_index()
                fig_avg = px.line(avg_daily, x="Date", y="Relevance Score",
                                  title="Average Relevance Score per Day", markers=True)
                fig_avg.update_traces(line_color="#dc2626")
                st.plotly_chart(fig_avg, use_container_width=True)

            if len(trend_df) >= 10:
                trend_df["DayOfWeek"] = trend_df["_createdTime"].dt.day_name()
                trend_df["Hour"] = trend_df["_createdTime"].dt.hour
                dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                pivot_hm = trend_df.groupby(["DayOfWeek", "Hour"]).size().reset_index(name="Count")
                pivot_hm = pivot_hm.pivot(index="DayOfWeek", columns="Hour", values="Count").fillna(0)
                pivot_hm = pivot_hm.reindex([d for d in dow_order if d in pivot_hm.index])
                fig_hm = px.imshow(pivot_hm,
                                   labels=dict(x="Hour (UTC)", y="Day", color="Threats"),
                                   color_continuous_scale="Reds", aspect="auto",
                                   title="Threat Ingestion by Day & Hour")
                st.plotly_chart(fig_hm, use_container_width=True)

# ----- MITRE ATT&CK -----
with tab_mitre:
    st.markdown("### MITRE ATT&CK Technique Mapping")
    st.caption("Techniques are extracted from threat titles and summaries by matching T-ID patterns (e.g. T1566).")
    all_techniques = [t for techs in filtered_df["_mitre"] for t in techs]
    if not all_techniques:
        st.info("No MITRE ATT&CK technique IDs detected. Have your AI pipeline tag summaries with technique IDs (e.g. 'T1566.001') for this view to populate.")
    else:
        tech_series = pd.Series(all_techniques)
        tech_counts = tech_series.value_counts().reset_index()
        tech_counts.columns = ["Technique ID", "Count"]
        tech_counts["Technique Name"] = tech_counts["Technique ID"].apply(
            lambda t: MITRE_TECHNIQUES.get(t.split(".")[0], "Unknown technique"))
        tech_counts["Label"] = tech_counts["Technique ID"] + " — " + tech_counts["Technique Name"]
        tech_counts["Link"] = tech_counts["Technique ID"].apply(
            lambda t: f"https://attack.mitre.org/techniques/{t.replace('.', '/')}/")

        c1, c2 = st.columns([2, 1])
        with c1:
            top_n = min(15, len(tech_counts))
            fig_tech = px.bar(tech_counts.head(top_n), x="Count", y="Label",
                              orientation="h", title=f"Top {top_n} ATT&CK Techniques",
                              color="Count", color_continuous_scale="Reds")
            fig_tech.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig_tech, use_container_width=True)
        with c2:
            st.markdown("**Technique References**")
            for _, row in tech_counts.head(10).iterrows():
                st.markdown(f"- [{row['Technique ID']}]({row['Link']}) — {row['Technique Name']} (×{row['Count']})")

        st.markdown("#### Threats by Technique")
        selected_tech = st.selectbox("Filter threats by technique", ["All"] + tech_counts["Technique ID"].tolist())
        if selected_tech != "All":
            tech_threats = filtered_df[filtered_df["_mitre"].apply(lambda techs: selected_tech in techs)]
            st.dataframe(tech_threats[["Title", "_priority_effective", "Severity Level", "Relevance Score"]]
                         .rename(columns={"_priority_effective": "Priority"}),
                         use_container_width=True, hide_index=True)

# ----- THREAT TABLE -----
with tab_table:
    st.markdown("### Actionable Threats")
    st.caption(f"Showing {len(filtered_df)} threats")
    table_df = filtered_df.copy()
    table_df["CVEs"] = table_df["_cves"].apply(lambda lst: ", ".join(lst[:3]) if lst else "—")
    table_df["TTPs"] = table_df["_mitre"].apply(lambda lst: ", ".join(lst[:3]) if lst else "—")
    table_df["Priority"] = table_df["_priority_effective"]
    display_cols = ["Title", "Relevance Score", "Priority", "Severity Level",
                    "Affected Software", "CVEs", "TTPs"]
    display_df = table_df[[c for c in display_cols if c in table_df.columns]].copy()

    def color_severity(val):
        c = SEVERITY_COLORS.get(str(val), "#6b7280")
        return f"background-color: {c}; color: white; font-weight: bold; text-align: center;"
    def color_priority(val):
        c = PRIORITY_COLORS.get(str(val), "#6b7280")
        return f"background-color: {c}; color: white; font-weight: bold; text-align: center;"
    def color_score(val):
        try: v = float(val)
        except (TypeError, ValueError): return ""
        if v >= 80: return "background-color: #dc2626; color: white; font-weight: bold;"
        if v >= 60: return "background-color: #ea580c; color: white; font-weight: bold;"
        if v >= 40: return "background-color: #ca8a04; color: white; font-weight: bold;"
        return "background-color: #16a34a; color: white;"

    # Styler.applymap was renamed to Styler.map in pandas 2.1
    def apply_style(styler, fn, col):
        if hasattr(styler, "map"):
            return styler.map(fn, subset=[col])
        return styler.applymap(fn, subset=[col])

    styled = display_df.style
    styled = apply_style(styled, color_severity, "Severity Level")
    styled = apply_style(styled, color_priority, "Priority")
    styled = apply_style(styled, color_score, "Relevance Score")
    styled = styled.format({"Relevance Score": "{:.0f}"})
    st.dataframe(styled, use_container_width=True, hide_index=True, height=500)

# ----- DEEP DIVE -----
with tab_dive:
    st.markdown("### Threat Deep Dive")
    threat_titles = filtered_df["Title"].dropna().unique().tolist()
    if not threat_titles:
        st.info("No threats match the current filters.")
    else:
        selected_threat = st.selectbox("Select a Threat", threat_titles)
        details = filtered_df[filtered_df["Title"] == selected_threat].iloc[0]

        priority = details.get("_priority_effective", "N/A")
        severity = details.get("Severity Level", "N/A")
        score = float(details.get("Relevance Score", 0))

        b1, b2, b3 = st.columns(3)
        b1.markdown(f"<div style='background:{PRIORITY_COLORS.get(priority, '#6b7280')};"
                    f"padding:1rem;border-radius:8px;text-align:center;color:white;'>"
                    f"<strong>Priority</strong><br/>{priority}</div>", unsafe_allow_html=True)
        b2.markdown(f"<div style='background:{SEVERITY_COLORS.get(severity, '#6b7280')};"
                    f"padding:1rem;border-radius:8px;text-align:center;color:white;'>"
                    f"<strong>Severity</strong><br/>{severity}</div>", unsafe_allow_html=True)
        b3.markdown(f"<div style='background:#1f2937;padding:1rem;border-radius:8px;"
                    f"text-align:center;color:white;'>"
                    f"<strong>Relevance Score</strong><br/>{score:.0f} / 100</div>", unsafe_allow_html=True)

        st.markdown("")
        st.info(f"**Affected Software:** {details.get('Affected Software', 'Unknown')}")
        st.markdown("#### AI Summary")
        st.write(details.get("Summary", "No summary available."))

        threat_techs = details.get("_mitre", [])
        if threat_techs:
            st.markdown("#### MITRE ATT&CK Techniques")
            for t in threat_techs:
                name = MITRE_TECHNIQUES.get(t.split(".")[0], "Unknown technique")
                url = f"https://attack.mitre.org/techniques/{t.replace('.', '/')}/"
                st.markdown(f"- [`{t}`]({url}) — {name}")

        threat_cves = details.get("_cves", [])
        if threat_cves:
            st.markdown("#### CVE Enrichment (NVD)")
            for cve in threat_cves[:5]:
                with st.expander(f"📌 {cve}"):
                    info = fetch_nvd_cve(cve)
                    if not info:
                        st.warning(f"Could not retrieve data for {cve}.")
                        continue
                    cc1, cc2, cc3 = st.columns(3)
                    cvss = info.get("cvss_score")
                    sev_nvd = info.get("severity") or "Unknown"
                    sev_color_nvd = SEVERITY_COLORS.get(sev_nvd.title(), "#6b7280")
                    cc1.markdown(f"<div style='background:{sev_color_nvd};padding:0.75rem;border-radius:6px;"
                                 f"text-align:center;color:white;'><strong>CVSS</strong><br/>{cvss if cvss else '—'}</div>",
                                 unsafe_allow_html=True)
                    cc2.markdown(f"<div style='background:{sev_color_nvd};padding:0.75rem;border-radius:6px;"
                                 f"text-align:center;color:white;'><strong>NVD Severity</strong><br/>{sev_nvd}</div>",
                                 unsafe_allow_html=True)
                    cc3.markdown(f"<div style='background:#1f2937;padding:0.75rem;border-radius:6px;"
                                 f"text-align:center;color:white;'><strong>Published</strong><br/>"
                                 f"{(info.get('published') or '')[:10] or '—'}</div>", unsafe_allow_html=True)
                    if info.get("vector"): st.caption(f"Vector: `{info['vector']}`")
                    if info.get("description"): st.write(info["description"])
                    st.markdown(f"[View on NVD →]({info['link']})")

        st.markdown("#### Send Alert for This Threat")
        a1, a2 = st.columns(2)
        with a1:
            if st.button("💬 Send to Slack", key="dive_slack"):
                ok, msg = send_slack_alert(f"🚨 {priority} threat: {selected_threat}",
                                            blocks=build_slack_blocks_for_threat(details))
                if ok:
                    st.success("Sent to Slack")
                    st.session_state.alert_log.append({"time": datetime.now(), "channel": "Slack", "target": selected_threat})
                else: st.error(f"Failed: {msg}")
        with a2:
            if st.button("📧 Send to Email", key="dive_email"):
                single_df = pd.DataFrame([details])
                ok, msg = send_email_alert(f"🚨 Threat Intel Alert: {selected_threat[:60]}",
                                            build_email_html_for_threats(single_df))
                if ok:
                    st.success("Email sent")
                    st.session_state.alert_log.append({"time": datetime.now(), "channel": "Email", "target": selected_threat})
                else: st.error(f"Failed: {msg}")

        with st.expander("All fields"):
            for col, val in details.items():
                if not col.startswith("_") and pd.notna(val) if not isinstance(val, list) else val:
                    st.write(f"**{col}:** {val}")

# ----- ALERTS -----
with tab_alerts:
    st.markdown("### Alert Configuration & Dispatch")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Slack")
        if SLACK_WEBHOOK_URL:
            st.success("✅ Slack webhook configured")
        else:
            st.warning("⚠️ No Slack webhook in secrets")
            with st.expander("How to set up Slack alerts"):
                st.code('SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T.../B.../..."', language="toml")
        if st.button("📨 Send Slack Test"):
            ok, msg = send_slack_alert("✅ Threat Intel Dashboard test alert — connection verified.")
            if ok: st.success("Test sent")
            else: st.error(f"Failed: {msg}")

    with c2:
        st.markdown("#### Email (SMTP)")
        smtp_ready = all([SMTP_HOST, SMTP_USER, SMTP_PASS, ALERT_TO_EMAIL])
        if smtp_ready:
            st.success(f"✅ SMTP configured ({SMTP_HOST}) → {ALERT_TO_EMAIL}")
        else:
            st.warning("⚠️ SMTP credentials incomplete")
            with st.expander("How to set up email alerts"):
                st.code('''SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "you@gmail.com"
SMTP_PASS = "your-16-char-app-password"
ALERT_TO_EMAIL = "soc@example.com"''', language="toml")
        if st.button("📨 Send Email Test"):
            ok, msg = send_email_alert("Threat Intel Dashboard — Test Alert",
                                       "<p>✅ Connection verified.</p>")
            if ok: st.success("Test sent")
            else: st.error(f"Failed: {msg}")

    st.divider()
    st.markdown("#### Bulk Dispatch")
    crit_threats = filtered_df[filtered_df["_priority_effective"] == "Critical"]
    high_threats = filtered_df[filtered_df["_priority_effective"].isin(["Critical", "High"])]
    st.caption(f"{len(crit_threats)} Critical / {len(high_threats)} Critical+High in current filter.")

    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1:
        if st.button(f"💬 Slack all Critical ({len(crit_threats)})"):
            sent, failed = 0, 0
            for _, t in crit_threats.iterrows():
                ok, _ = send_slack_alert(f"🚨 Critical: {t['Title']}",
                                          blocks=build_slack_blocks_for_threat(t))
                if ok: sent += 1
                else: failed += 1
            st.success(f"Slack: sent {sent}, failed {failed}")
    with bc2:
        if st.button(f"📧 Email all Critical ({len(crit_threats)})"):
            if not crit_threats.empty:
                ok, msg = send_email_alert(f"🚨 {len(crit_threats)} Critical Threats",
                                           build_email_html_for_threats(crit_threats))
                if ok: st.success("Email sent")
                else: st.error(f"Failed: {msg}")
            else: st.info("No Critical threats.")
    with bc3:
        if st.button(f"💬 Slack Critical+High ({len(high_threats)})"):
            sent, failed = 0, 0
            for _, t in high_threats.iterrows():
                ok, _ = send_slack_alert(f"🚨 {t['_priority_effective']}: {t['Title']}",
                                          blocks=build_slack_blocks_for_threat(t))
                if ok: sent += 1
                else: failed += 1
            st.success(f"Slack: sent {sent}, failed {failed}")
    with bc4:
        if st.button(f"📧 Email Critical+High ({len(high_threats)})"):
            if not high_threats.empty:
                ok, msg = send_email_alert(f"🚨 {len(high_threats)} Critical & High Threats",
                                           build_email_html_for_threats(high_threats))
                if ok: st.success("Email sent")
                else: st.error(f"Failed: {msg}")

    st.divider()
    st.markdown("#### Recent Alert Log (this session)")
    if st.session_state.alert_log:
        log_df = pd.DataFrame(st.session_state.alert_log)
        log_df["time"] = log_df["time"].astype(str)
        st.dataframe(log_df.iloc[::-1], use_container_width=True, hide_index=True)
        if st.button("Clear log"):
            st.session_state.alert_log = []
            st.rerun()
    else:
        st.caption("No alerts sent yet in this session.")

# ----- EXPORT -----
with tab_export:
    st.markdown("### Export Filtered Data")
    st.write(f"Export {len(filtered_df)} filtered threats")
    export_df = filtered_df.drop(columns=["_createdTime", "_cves", "_mitre",
                                          "_priority_effective", "_priority_fallback_used"],
                                  errors="ignore").copy()
    export_df["CVEs"] = filtered_df["_cves"].apply(lambda lst: ", ".join(lst))
    export_df["MITRE Techniques"] = filtered_df["_mitre"].apply(lambda lst: ", ".join(lst))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button("📥 Download CSV", data=export_df.to_csv(index=False),
                       file_name=f"threat_intel_{stamp}.csv", mime="text/csv")
    st.download_button("📥 Download JSON", data=export_df.to_json(orient="records", indent=2),
                       file_name=f"threat_intel_{stamp}.json", mime="application/json")
