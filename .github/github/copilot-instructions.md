# Capstone Project Context

## Project
- **Name:** AI-Capstone-Threat-Intel
- **Project type:** Automated Threat Intelligence Hub / Streamlit Threat Intelligence Dashboard
- **Team / components:**
  - Mathews and Darius — Component 1: Feed Collector / Ingestion
  - Ayman and Mathews — Component 2: AI Summarizer and IOC Extractor / AI Core
  - Barry and Uyi — Component 3: Relevance Scorer / Specialist
  - Integration team — Component 4: Dashboard, testing, documentation, and presentation
- **What it does:** The system collects threat intelligence from public sources, enriches the records with AI-generated summaries and IOC extraction, scores each item for relevance, and displays prioritized threats in a local Streamlit dashboard. The goal is to reduce manual triage work for analysts by turning RSS/CVE/OTX source data into a ranked threat feed.

## Current Local Run Setup
The current project state is based on the local run package tested for the Streamlit Threat Intelligence Dashboard.

### n8n Workflows
1. **Feed Collector - Krebs RSS to Airtable - Fixed**
   - Pulls Krebs RSS entries.
   - Normalizes title, source, description, URL, and publication metadata.
   - Writes collected records to Airtable.
2. **Feed Collector - NVD CVE to Airtable**
   - Pulls CVE/vulnerability records from NVD-style data.
   - Writes CVE-related threat records to Airtable.
3. **AlienVault OTX Workflow**
   - Pulls AlienVault OTX pulse/indicator data.
   - Writes OTX records to Airtable / the OTX CSV export.
4. **AI Summarizer - Krebs and CVD**
   - Processes Krebs and CVE/CVD-style records.
   - Produces summaries and structured analysis fields.
5. **AlienVault OTX - Flowise IOC Extractor and Summarizer**
   - Uses Flowise/Groq to summarize OTX records.
   - Extracts IOCs and writes enriched analysis output.

### Airtable CSV Exports
The local dashboard/test setup uses these Airtable CSV exports:
- `Threats-Grid view.csv`
- `Sources-Grid view.csv`
- `AlienVault_OTX-Grid view.csv`

### Dashboard
- The integration component is a local Streamlit threat intelligence dashboard.
- It loads Airtable/exported CSV data and displays prioritized threat records.
- It supports relevance score filtering through the Relevance Score Range control.
- It includes CSV enrichment behavior that can populate dashboard-facing fields such as summary, severity, relevance score, priority ranking, and affected software.
- Known issue: the dashboard currently prints repeated terminal/log messages when the dashboard instantiates, when the Relevance Score Range changes, and when CSV enrichment runs. These messages are noisy but not considered a data-processing failure.

## Architecture
- **Ingestion:** n8n feed collector workflows pull from Krebs RSS, NVD CVE/CVD-style feeds, and AlienVault OTX. They write normalized threat records to Airtable tables and CSV exports.
- **AI Core:** n8n and Flowise/Groq workflows summarize records and extract structured IOCs, severity, affected software, and threat context.
- **Specialist / Relevance Scorer:** Records are scored for organizational relevance. The scorer considers severity, affected software, IOC presence, recency, and keyword matches against the dashboard's operational priority logic.
- **Integration Dashboard:** A local Streamlit dashboard loads Airtable/CSV data, applies filtering and enrichment, and presents the prioritized threat feed.

## Tech Stack
- n8n Cloud / n8n local workflow automation
- Flowise Cloud or local Flowise for LLM chains
- Groq API for LLM inference
- Airtable for shared data storage and CSV exports
- Streamlit for the local dashboard
- Python for dashboard processing and CSV enrichment
- GitHub for repository documentation and portfolio evidence

## Airtable / CSV Schema Notes
The current tables/exports are not perfectly unified, so field names may differ slightly by source. When writing n8n expressions or dashboard code, use exact field names from the live Airtable output.

### Threats / Threats-Grid view.csv
| Field | Purpose | Written By |
|---|---|---|
| Title | Main threat title | Feed Collector |
| Source | Source or feed name | Feed Collector |
| URL | Source URL / advisory URL | Feed Collector |
| Published At | Publication timestamp | Feed Collector |
| Raw Description | Original source text | Feed Collector |
| Summary | AI-generated summary | AI Core |
| Severity Level | AI or source severity | AI Core / Relevance Scorer |
| Affected Software | Products or systems affected | AI Core / Relevance Scorer |
| Relevance Score | Numeric relevance score | Relevance Scorer / dashboard enrichment |
| Priority Ranking | Human-readable priority tier | Relevance Scorer / dashboard enrichment |

### Sources / Sources-Grid view.csv
| Field | Purpose | Written By |
|---|---|---|
| Source Name | Feed/source label | Integration / Feed Collector |
| Source Type | RSS, CVE, OTX, manual, etc. | Integration / Feed Collector |
| Feed URL | Public feed/API endpoint or source page | Integration / Feed Collector |
| Status | Enabled/disabled or collection status | Integration |

### AlienVault_OTX / AlienVault_OTX-Grid view.csv
| Field | Purpose | Written By |
|---|---|---|
| Pulse Name / Title | OTX pulse title | AlienVault OTX Workflow |
| Description | Raw OTX description | AlienVault OTX Workflow |
| Indicator | IOC value when available | AlienVault OTX Workflow / AI Core |
| Indicator Type | Domain, IP, URL, hash, CVE, etc. | AlienVault OTX Workflow / AI Core |
| Summary | Flowise/Groq summary | OTX Flowise workflow |
| IOC Summary | Structured IOC explanation | OTX Flowise workflow |
| Severity Level | AI/source severity | AI Core / scorer |
| Relevance Score | Dashboard/scorer relevance | Relevance Scorer / dashboard enrichment |
| Priority Ranking | Dashboard/scorer priority | Relevance Scorer / dashboard enrichment |

## Conventions
- Do not commit API keys, Airtable personal access tokens, Flowise keys, Groq keys, or `.streamlit/secrets.toml`.
- Keep public screenshots free of visible bearer tokens, API URLs with private IDs, and credential panels.
- Use documentation-safe examples such as `evil-domain.example`, `203.0.113.45`, and `workstation-47`.
- Treat exact Airtable field names as integration contracts because n8n expressions are case-sensitive and space-sensitive.

## Current State After Checkpoint 2 Local Run
- **What's working:** The project has working source-specific n8n workflows for Krebs RSS, NVD/CVE data, AlienVault OTX collection, Krebs/CVE summarization, and OTX Flowise IOC extraction/summarization. The local Streamlit dashboard runs and can display/enrich threat data from Airtable/CSV exports. The relevance score filter and CSV enrichment path are functional enough for Checkpoint 2 evidence.
- **What's partially working:** The full pipeline exists as connected stages, but not yet as one clean master orchestration that automatically moves one record through every component from a single trigger. Some evidence comes from exported Airtable CSV files and local dashboard enrichment rather than one always-on production pipeline.
- **Known issues:** The dashboard produces repeated terminal/log output during initialization, Relevance Score Range changes, and CSV enrichment. Handoffs are source-specific, and field naming consistency across Threats, Sources, and AlienVault OTX exports is still a risk. The dashboard depends on local configuration and/or Airtable credentials that must stay out of GitHub.
- **Next milestone:** Week 10 should focus on productionizing the pipeline: unified status fields, confidence-based routing, clearer error handling, a master orchestration workflow, and a cleaner dashboard logging strategy.

## Repository Structure
```text
AI-Capstone-Threat-Intel/
├── .github/
│   └── copilot-instructions.md
├── component-1-feed-collector/
├── component-2-ai-summarizer/
├── component-3-relevance-scorer/
├── component-4-integration/
├── data/
├── docs/
│   ├── checkpoint2-results.md
│   ├── checkpoint2-audit.md
│   └── week9-local-run-submission-guide.md
├── screenshots/
└── prompt-log-ren.md
```

## Guidance for Copilot
When helping with this project:
- Use the current local run setup above as the source of truth.
- Be specific about which n8n workflow handles which source.
- Do not invent hidden credentials or assume all components are fully production-integrated.
- Prefer honest status labels: Working, Partially Working, Not Working.
- For Checkpoint 2, explain the current system as a partial end-to-end integration with working source-specific stages and a working local dashboard, not as a fully autonomous production pipeline.
