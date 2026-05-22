# Week 10 Lab: Phase 4 — Error Handling, Routing & Dashboard

**Name:** Darius  
**Project:** AI-Capstone-Threat-Intel  
**Date:** May 21, 2026  
**Live Dashboard:** https://ai-capstone-threat-intelligence-dashboard.streamlit.app/  
**Project status:** The capstone pipeline is complete, working end-to-end, and the Streamlit dashboard is live.

## Part 1: Error Handling

### Error scenario handled

For my component, I handled **bad input data in the Feed Collector / Ingestion stage**. The pipeline receives threat intelligence records from public sources such as AlienVault OTX, Krebs, and NVD. A bad record can be missing required fields, contain an empty IOC/CVE/indicator field, have a malformed URL, or have incomplete source metadata. Before this update, a malformed record could stop clean processing or simply fail to move through the rest of the workflow.

### What I built

I added a validation branch in the n8n ingestion workflow before records are sent into the scoring and enrichment path. The workflow now checks whether the required fields are present. Valid records continue into the normal processing path. Invalid records are still written to Airtable, but they are marked with:

- `status = error`
- `error_reason = Missing required IOC/indicator field; record cannot be scored or routed.`

This prevents silent record loss and gives the dashboard an error record that can be reviewed later.

## Part 2: Confidence-Based Routing / Equivalent Routing Logic

### Routing logic used

My project uses threat-intelligence relevance scoring rather than a generic confidence score, so I implemented the equivalent routing logic using `relevance_score`.

After the relevance scorer parses the model output, an n8n IF node checks:

```text
relevance_score >= 70
```

### Why I chose this threshold

I chose a threshold of **70 out of 100** because it is high enough to keep low-value or generic security news out of the automatic action path, but not so strict that meaningful threat intelligence with useful indicators gets delayed unnecessarily.

## Part 3: Dashboard Progress

### Dashboard view 1: Pipeline Status

**Screenshot:** `screenshots/week10-dashboard-pipeline-status.png`

This view shows records grouped or filtered by processing status, such as unprocessed, analyzed, needs_review, and error. It is for the whole team because it quickly shows whether the pipeline is moving records through each stage correctly.

### Dashboard view 2: Error Monitor

**Screenshot:** `screenshots/week10-dashboard-error-monitor.png`

This view shows only records where `status = error`, including the `error_reason` field. It is for whoever is debugging the pipeline because it identifies malformed inputs, API failures, or downstream action failures without requiring the team to inspect every workflow execution manually.

