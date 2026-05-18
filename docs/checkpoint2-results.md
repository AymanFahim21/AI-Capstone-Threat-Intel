# Checkpoint 2 Results

**Date:** 2026-05-17  
**Team:** AI-Capstone-Threat-Intel  
**Test record:** Outbound DNS beaconing from `workstation-47` to suspicious command-and-control infrastructure.  

## Test Record Details

**What it is:** A realistic cybersecurity threat intelligence record describing repeated DNS queries from an internal workstation to suspicious randomized subdomains. This record is intended to test whether the system can collect a raw threat item, classify/analyze it, score its relevance, recommend a response, and show it in the dashboard.

**Expected path:** Feed Collector / Ingestion writes the record to Airtable → AI Core summarizes and extracts indicators → Specialist / Relevance Scorer scores the record and recommends priority/action → Integration dashboard displays the completed record.

**Expected final state:** The completed Airtable record should have `ingestion_status = collected`, `ai_status = summarized`, `scoring_status = scored`, populated AI fields, a high or critical priority, and a visible dashboard entry.

### Clean Test Input

```text
Title: Outbound DNS beaconing detected from workstation-47
Source name: Manual Checkpoint 2 Test
Source type: manual_test
Source URL: https://example.com/checkpoint2-dns-beaconing-test
Raw description: Workstation-47 generated outbound DNS queries every 30 seconds to randomized subdomains of suspicious-control.example. The pattern began after a successful login from 203.0.113.45 and may indicate command-and-control beaconing, malware persistence, or post-compromise activity.
Normalized text: Workstation-47 is repeatedly querying randomized subdomains of suspicious-control.example every 30 seconds after a suspicious successful login from 203.0.113.45.
```

## End-to-End Status: PARTIAL

At the time this file was prepared, the Week 8 Flowise/n8n API chain was working, but the full Checkpoint 2 Airtable-based capstone handoff still needed to be run and documented. After running the test, update the status to `PASSED`, `PARTIAL`, or `FAILED` based on what actually happened.

## Component-by-Component Results

### Ingestion

- **Status:** To verify during test run
- **What happened:** The Feed Collector should create a new Airtable record in the `threats` table using the clean test input. The record should include source metadata, raw description, normalized text, `ingestion_status = collected`, and `ai_status = pending_ai`.
- **Screenshot:** `screenshots/checkpoint2-1-ingestion.png`

### AI Core

- **Status:** To verify during test run
- **What happened:** The AI Core should pick up the record marked `ai_status = pending_ai`, generate a summary, classify severity, identify the attack type, extract indicators of compromise, and update the record to `ai_status = summarized` with `scoring_status = pending_scoring`.
- **Screenshot:** `screenshots/checkpoint2-2-ai-core.png`

### Specialist / Relevance Scorer

- **Status:** To verify during test run
- **What happened:** The Specialist/Relevance Scorer should process the AI-enriched record, compare it against the organization technology stack or relevance criteria, write a relevance score, assign a priority, add a short explanation and recommended action, and update `scoring_status = scored`.
- **Screenshot:** `screenshots/checkpoint2-3-specialist.png`

### Integration Dashboard

- **Status:** To verify during test run
- **What happened:** The completed record should be visible in the dashboard or Airtable view used by the Integration component. The dashboard should show the title, source, severity, priority, relevance score, summary, and recommended action.
- **Screenshot:** `screenshots/checkpoint2-4-dashboard.png`

## Gaps Found

Update this section after the test run. Current expected gaps to watch for:

- If the AI workflow does not pick up the Ingestion record, check whether `ai_status` exactly equals `pending_ai`.
- If the Specialist workflow does not run, check whether AI Core writes `scoring_status = pending_scoring` exactly.
- If the dashboard does not show the record, check whether the dashboard view is filtering out incomplete or newly created records.
- If n8n expressions fail, check exact Airtable field names and remove trailing spaces from field names.
- If a Flowise request fails, verify the prediction URL, API key/header setup, and whether the chain runner is saved and tested in Flowise.

## Fix Plan

1. **Confirm the shared Airtable fields exist.** Owner: Integration / all components. Estimated effort: 30-60 minutes. Create or verify the `threats` fields listed in `.github/copilot-instructions.md`.
2. **Run the clean test record through Ingestion.** Owner: Feed Collector. Estimated effort: 30 minutes. Confirm the record appears in Airtable with `ai_status = pending_ai`.
3. **Verify AI Core auto-pickup.** Owner: AI Core. Estimated effort: 60-90 minutes. Confirm AI fields populate and status advances to `scoring_status = pending_scoring`.
4. **Verify Specialist scoring.** Owner: Relevance Scorer. Estimated effort: 60-90 minutes. Confirm relevance score, priority, explanation, and recommended action are written.
5. **Verify dashboard visibility.** Owner: Integration. Estimated effort: 30 minutes. Confirm the final record appears in the dashboard view and screenshot it.
6. **Update this results report.** Owner: Ren / submitting student. Estimated effort: 20 minutes. Replace `To verify during test run` lines with what actually happened.
