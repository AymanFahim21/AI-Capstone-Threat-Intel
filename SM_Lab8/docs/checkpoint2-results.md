# Checkpoint 2 Results

**Date:** 2026-05-21  
**Team:** AI-Capstone-Threat-Intel  
**Test record:** AlienVault OTX / threat-feed record representing command-and-control style IOC activity, used to verify collection, AI enrichment, relevance scoring, and dashboard visibility.

## End-to-End Status: PARTIAL

The project has a working local integration path, but it is not yet a fully productionized one-trigger end-to-end system. The local run setup demonstrates all four required stages: feed collection into Airtable/CSV exports, AI summarization and IOC extraction, relevance scoring / CSV enrichment, and display inside the Streamlit dashboard. The remaining gap is that these stages are still source-specific workflows and local dashboard/enrichment steps rather than one master workflow that automatically advances a single record through every component without any manual trigger or exported-file handoff.

This is a valid Checkpoint 2 result because the purpose of the lab is to document what works and what breaks during the end-to-end attempt, not to pretend the system has no gaps.

## Test Record Details

**What it is:** A realistic threat intelligence record from the AlienVault OTX / public threat-feed side of the project. The record represents suspicious command-and-control or malicious-domain activity and contains enough source text for AI summarization, IOC extraction, relevance scoring, and dashboard display.

**Expected path:**

```text
AlienVault OTX Workflow or Feed Collector workflow
→ Airtable / exported CSV record
→ AlienVault OTX - Flowise IOC Extractor and Summarizer or AI Summarizer workflow
→ Relevance Scorer / dashboard CSV enrichment
→ Streamlit Threat Intelligence Dashboard
```

**Expected final state:** The record should be visible in the dashboard with a title, source context, summary, severity level, affected software or IOC context, relevance score, and priority ranking.

## Component-by-Component Results

### Ingestion

- **Status:** Working
- **What happened:** The local run setup includes source-specific n8n ingestion workflows: `Feed Collector - Krebs RSS to Airtable - Fixed`, `Feed Collector - NVD CVE to Airtable`, and `AlienVault OTX Workflow`. These workflows collect public threat intelligence from RSS/CVE/OTX sources and write normalized records into Airtable and the exported CSV files used by the dashboard.
- **Evidence to screenshot:** Show the newly collected or selected test record in Airtable or the relevant CSV export after the collector workflow runs. The screenshot should show the record title/source/description fields, not credential panels.
- **Screenshot:** `screenshots/checkpoint2-1-ingestion.png`

### AI Core

- **Status:** Working
- **What happened:** The local run setup includes `AI Summarizer - Krebs and CVD` and `AlienVault OTX - Flowise IOC Extractor and Summarizer`. These workflows enrich collected threat records by producing summaries, extracting IOC context, and preparing dashboard-facing analysis fields. For an OTX test record, the OTX Flowise summarizer is the clearest AI Core evidence.
- **Evidence to screenshot:** Show the same or equivalent test record after AI output is populated. Acceptable evidence includes the n8n execution output, Airtable fields, or CSV fields showing summary/IOC/severity output.
- **Screenshot:** `screenshots/checkpoint2-2-ai-core.png`

### Specialist / Relevance Scorer

- **Status:** Partially Working
- **What happened:** The relevance scoring stage exists through the local dashboard/enrichment path and the Relevance Score Range behavior. The system can compute or display `Relevance Score`, `Priority Ranking`, `Severity Level`, `Affected Software`, and `Summary` fields for dashboard triage. This proves the specialist function conceptually works, but the scorer is not yet documented as a single autonomous production handoff that always writes back to Airtable for every source type.
- **Evidence to screenshot:** Show the test record after CSV enrichment or scoring, with relevance score and priority fields visible. If the score is visible only in the dashboard rather than Airtable, screenshot the dashboard table/card containing the score.
- **Screenshot:** `screenshots/checkpoint2-3-specialist.png`

### Integration Dashboard

- **Status:** Working with known issues
- **What happened:** The local Streamlit dashboard loads the threat intelligence data, displays enriched records, and supports filtering by relevance score. The dashboard is usable for Checkpoint 2 evidence. The known issue is terminal/log noise during initialization, relevance range changes, and CSV enrichment runs; this is a logging/UI polish issue, not a complete dashboard failure.
- **Evidence to screenshot:** Show the test record visible in the dashboard. The screenshot should include the dashboard table/card and, if possible, the Relevance Score Range filter or enriched fields.
- **Screenshot:** `screenshots/checkpoint2-4-dashboard.png`

## Gaps Found

- **No single master orchestration workflow yet.** The project currently works as multiple source-specific n8n workflows plus a local dashboard/enrichment path. A fully automated production version should use one shared status contract or a master workflow to move records from collection to AI enrichment to scoring to dashboard readiness.
- **Dashboard depends on local setup and exported/live data configuration.** The dashboard works locally, but the repo should avoid committing `.streamlit/secrets.toml`, Airtable tokens, or private API details.
- **Field naming consistency remains a risk.** The three CSV exports and Airtable tables may not use identical field names. This can break n8n expressions or dashboard mappings.
- **Relevance scoring writeback needs polish.** The scorer/dashboard enrichment can populate relevance-facing fields, but the final production design should clearly write `Relevance Score` and `Priority Ranking` back to the authoritative Airtable record.
- **Terminal/log noise needs cleanup.** Repeated messages appear when the dashboard starts, when the Relevance Score Range changes, and when CSV enrichment runs.
- **Status fields are not yet a strong handoff contract.** A production flow should use explicit statuses such as `collected`, `ai_processed`, `scored`, and `dashboard_ready` across every workflow.

## Fix Plan

1. **Create a master handoff contract.** Owner: Integration team. Estimated effort: 1-2 hours. Define exact shared fields for `collection_status`, `ai_status`, `scoring_status`, and `dashboard_status` so every workflow knows what to read and write.
2. **Standardize field names across Airtable and CSV exports.** Owner: Integration + component owners. Estimated effort: 1-2 hours. Align `Title`, `Summary`, `Severity Level`, `Affected Software`, `Relevance Score`, and `Priority Ranking` across the Threats and OTX exports.
3. **Add scoring writeback to Airtable.** Owner: Relevance Scorer. Estimated effort: 1-2 hours. Ensure relevance score and priority are written back to the same record that AI Core enriched.
4. **Reduce dashboard logging noise.** Owner: Integration. Estimated effort: 30-60 minutes. Move repeated initialization/enrichment print statements behind a debug flag or Streamlit status panel.
5. **Add a dashboard-ready view.** Owner: Integration. Estimated effort: 30-60 minutes. Create a filtered Airtable/dashboard view showing only records with AI summary and relevance score populated.
6. **Document the one-record demo path.** Owner: submitting student / team. Estimated effort: 30 minutes. Keep the four screenshots and this results file updated so the final demo can be repeated.
