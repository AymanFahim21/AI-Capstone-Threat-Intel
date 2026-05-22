# Prompt Log — Mathews

**Project:** AI-Capstone-Threat-Intel  
**Team:** Threat Intelligence Feed Dashboard  
**My Component:** Component 1 — Feed Collector / Ingestion  
**AI Tools Used:** GitHub Copilot, ChatGPT, n8n workflow troubleshooting support

---

## How to Use This Log

This log tracks significant AI-assisted development interactions for the capstone project. Each entry records the context, prompt, result, evaluation, edits made, and what I learned. It does not include ordinary autocomplete suggestions.

---

## 2026-05-21 — Reviewed the Feed Collector role for Checkpoint 2

**Context:** I was preparing the Week 9 Checkpoint 2 submission and needed to clarify how the Feed Collector fits into the end-to-end pipeline.

**Prompt:**
> Using the AI-Capstone-Threat-Intel project context, explain the Feed Collector component’s role in the Checkpoint 2 end-to-end test. Identify what it should write to Airtable and what the next component needs from it.

**Result:** The AI described the Feed Collector as the ingestion stage that pulls threat data from public sources such as Krebs, NVD, and AlienVault OTX, normalizes records, and writes raw threat entries to Airtable. It identified fields such as title, source, date, raw description, URL, and processing status as important outputs.

**Evaluation:** The result matched the component goal. It helped distinguish ingestion fields from AI-generated fields and scoring fields.

**What I changed:** I used this breakdown to verify that the checkpoint documentation described Ingestion as the first stage and did not mix it with AI summarization or relevance scoring.

**What I learned:** Ingestion quality matters because every downstream step depends on clean, consistent raw records.

---

## 2026-05-21 — Checked the local ingestion workflows against the checkpoint requirement

**Context:** The local run setup included multiple n8n workflows: Krebs RSS to Airtable, NVD CVE to Airtable, and AlienVault OTX. I needed to identify which workflow best proves ingestion for the checkpoint.

**Prompt:**
> I have n8n workflows for Krebs RSS to Airtable, NVD CVE to Airtable, and AlienVault OTX. For a Checkpoint 2 integration test, which one is best for proving ingestion and what screenshot should I take?

**Result:** The AI recommended using the workflow that most clearly creates or updates an Airtable record with recognizable threat data. It suggested taking a screenshot of the executed n8n workflow and a screenshot of the resulting Airtable record after ingestion.

**Evaluation:** This was useful because the lab requires stage evidence, not just written claims. It also made it clear that the screenshot should show the record after ingestion before AI fields are added.

**What I changed:** I treated the ingestion screenshot as evidence of the raw record entering the system, not as evidence of the entire pipeline.

**What I learned:** A checkpoint screenshot should prove a specific stage, not just show a tool window.

---

## 2026-05-21 — Used AI to identify required Airtable fields for ingestion

**Context:** I needed to make sure the Feed Collector writes enough data for AI Core to pick up and process the record.

**Prompt:**
> For a threat intelligence Feed Collector that writes to Airtable, list the minimum fields needed for downstream AI summarization and relevance scoring. Include field purpose and common integration mistakes.

**Result:** The AI recommended fields including title, source, raw description, URL, published date, ingestion status, AI processing status, and a unique source identifier or URL to avoid duplicates. It also warned about inconsistent field names, missing raw description text, and status values that do not match downstream n8n filters.

**Evaluation:** The minimum field list was accurate. The warning about status values was especially relevant because n8n workflows often depend on exact filter conditions.

**What I changed:** I used the list to check whether the checkpoint record contained enough information for the AI Summarizer to process it.

**What I learned:** Status fields and raw text fields are the main handoff points between ingestion and AI processing.

---

## 2026-05-21 — Generated a realistic checkpoint test record for ingestion

**Context:** I needed one clean record to use for the Checkpoint 2 end-to-end test instead of relying on random feed data that might be too short or incomplete.

**Prompt:**
> Generate one realistic threat intelligence record that a Feed Collector could write to Airtable. It should include title, source, raw description, URL placeholder, published date, and initial processing status. The record should be useful for testing AI summarization and relevance scoring.

**Result:** The AI generated a DNS beaconing / command-and-control test record involving workstation-47 and suspicious outbound DNS queries to randomized subdomains.

**Evaluation:** The record was realistic enough to test the system and had sufficient details for AI Core and Relevance Scorer stages. It was better than a vague placeholder because it contained observable behavior and indicators.

**What I changed:** I kept the scenario but treated it as a checkpoint test record rather than a real live threat feed entry.

**What I learned:** Controlled test data is useful because live feeds can be unpredictable and may not trigger every part of the pipeline.

---

## 2026-05-21 — Re-ran the audit from the Feed Collector perspective

**Context:** The Week 9 lab required the audit report to reflect the current project state after the Checkpoint 2 integration attempt.

**Prompt:**
> Act as a capstone advisor. Review the Feed Collector/Ingestion part of AI-Capstone-Threat-Intel for Checkpoint 2 readiness. Identify what is working, what could break the handoff to AI Core, and what fixes should be prioritized.

**Result:** The AI identified that ingestion workflows exist for multiple sources, but the main integration risks are duplicate records, inconsistent normalized fields across sources, and status values that may not automatically trigger AI Core. It recommended standardizing field names and ensuring each ingested record has a clear processing status.

**Evaluation:** The result was accurate and aligned with the project’s partial integration status. It did not overstate the pipeline as fully automated.

**What I changed:** I used the suggested risks in the Checkpoint 2 gap list and fix plan.

**What I learned:** Ingestion is not complete until downstream components can reliably detect and process the records it creates.
