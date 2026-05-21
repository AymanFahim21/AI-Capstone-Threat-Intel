# Checkpoint 2 Audit — AI-Capstone-Threat-Intel

## Checkpoint 2 Readiness Assessment

### Status: AT RISK / PARTIAL

The project is no longer just a proposal. The local run setup shows a working multi-stage threat intelligence system with five n8n workflows, three Airtable CSV exports, AI summarization/IOC extraction, relevance scoring behavior, and a local Streamlit dashboard. However, the system is still at risk for Checkpoint 2 because the current implementation is a partial integration rather than one polished, autonomous, end-to-end production pipeline.

## What's Working

- The project scope is clear: collect public threat intelligence, enrich it with AI, score relevance, and display prioritized results.
- The repository is organized by component: Feed Collector, AI Summarizer/AI Core, Relevance Scorer/Specialist, and Integration/Dashboard.
- The local setup includes five working or importable n8n workflows:
  - `Feed Collector - Krebs RSS to Airtable - Fixed`
  - `Feed Collector - NVD CVE to Airtable`
  - `AlienVault OTX Workflow`
  - `AI Summarizer - Krebs and CVD`
  - `AlienVault OTX - Flowise IOC Extractor and Summarizer`
- The project has Airtable CSV exports for local dashboard/testing:
  - `Threats-Grid view.csv`
  - `Sources-Grid view.csv`
  - `AlienVault_OTX-Grid view.csv`
- The AI enrichment stage exists for Krebs/CVE-style data and AlienVault OTX data.
- The local Streamlit dashboard runs and can show dashboard-facing fields such as title, summary, severity, affected software, relevance score, and priority ranking.
- The relevance score range filter and CSV enrichment behavior are present in the dashboard.

## Critical Gaps

- **The system still needs a single repeatable demo path.** The team should be able to say: run this collector, run this AI workflow if not automatic, run this scorer/enrichment step, then open this dashboard view.
- **The project is not yet one master automated pipeline.** Multiple workflows work, but they are not yet fully unified by one status-driven orchestration design.
- **Field names may be inconsistent across Airtable/CSV exports.** This is the most likely cause of broken dashboard mappings and n8n expression failures.
- **The relevance scorer needs stronger writeback documentation.** It is clear that relevance score and priority are used by the dashboard, but the production design should explicitly write those fields back to the authoritative Airtable record.
- **Dashboard logging needs cleanup.** Repeated terminal messages occur during instantiation, relevance score filter changes, and CSV enrichment. This should be cleaned up before final presentation.
- **Sensitive configuration must stay out of GitHub.** The dashboard may require an Airtable personal access token in `.streamlit/secrets.toml`; that file must not be committed.

## Schema Issues Found

- `Threats-Grid view.csv`, `Sources-Grid view.csv`, and `AlienVault_OTX-Grid view.csv` may not share one universal schema.
- Dashboard-facing fields should be standardized around:
  - `Title`
  - `Source`
  - `URL`
  - `Summary`
  - `Severity Level`
  - `Affected Software`
  - `Relevance Score`
  - `Priority Ranking`
- Any n8n node referencing Airtable fields must match exact capitalization and spacing.
- Future workflow fields should use explicit handoff values such as `collected`, `ai_processed`, `scored`, and `dashboard_ready`.

## Recommended Fix Order

1. **Pick one official Checkpoint 2 record.** Use either one AlienVault OTX pulse or one Krebs/NVD record visible in the current Airtable/CSV export.
2. **Capture the four evidence screenshots.** Ingestion, AI Core, Specialist/Relevance Scorer, and Dashboard.
3. **Update `docs/checkpoint2-results.md` with the exact record title shown in the screenshots.**
4. **Standardize dashboard-facing field names.** Make sure every component can produce or map into the same fields.
5. **Add status fields for handoff control.** This is the highest-value Week 10 improvement.
6. **Clean dashboard logs.** Keep only meaningful user-facing errors and move debug output behind a flag.

## Test Data Gaps

- The current data covers real public threat sources, but the team should add a small controlled set of test records covering:
  - A high-severity IOC/OTX record
  - A CVE affecting common software
  - A low-priority informational record
  - A malformed record with missing description
  - A duplicate or near-duplicate source entry

## Overall Assessment

The project is acceptable for a Checkpoint 2 partial integration submission if the screenshots clearly show one record moving through the available local stages. The strongest submission angle is honesty: the capstone has working component stages and a working dashboard, but still needs a unified automated handoff layer before the final demo.
