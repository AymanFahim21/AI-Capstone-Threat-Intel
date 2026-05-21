# Capstone Project Context

## Project

- **Name:** AI-Capstone-Threat-Intelligence-Dashboard
- **Team:** 
  - Sangram Mathews — Feed Collector / Ingestion
  - Ayman Fahim — IOC extractor and Summarizer / Threat Intelligence Processing
  - Darius Taule — Integration / Documentation and Workflow Support
- **What it does:** This project collects cybersecurity threat intelligence data, processes it using AI tools, and organizes the results for analysis. The system is designed to help security analysts summarize threat reports, classify alerts, extract indicators of compromise, and recommend response actions.
- **Project type:** AI-powered Threat Intelligence Dashboard and Workflow Automation System

## Architecture

- **Ingestion:** Threat intelligence data is collected from sources such as security feeds, CVE/NVD data, AlienVault OTX, Krebs/security blogs, or manually entered test alerts. n8n workflows are used to pull or send data between tools.
- **AI Core:** Flowise LLM chains and AI models classify alerts, analyze threat indicators, summarize threat reports, and recommend security response actions. Groq is used for LLM inference with the `llama-3.3-70b-versatile` model.
- **Integration:** n8n connects Flowise chains, APIs, Airtable, and GitHub documentation. The repository stores workflows, screenshots, documentation, and lab deliverables.

## Tech Stack

- n8n Cloud for workflow automation
- Flowise Cloud for LLM chains
- Groq API for LLM inference using `llama-3.3-70b-versatile`
- Hugging Face Inference API for AI model support
- Airtable for storing threat intelligence records
- GitHub for documentation, screenshots, workflow files, and portfolio evidence
- VS Code with GitHub Copilot for AI-assisted development

## Airtable Schema

The project may include tables such as:

### Threats

| Field | Type | Written By | Status Values |
|---|---|---|---|
| threat_title | text | Ingestion | N/A |
| source_name | text | Ingestion | N/A |
| source_url | url | Ingestion | N/A |
| summary | long text | AI Core | N/A |
| severity_level | single select | AI Core | low, medium, high, critical |
| attack_type | text | AI Core | N/A |
| cve_ids | long text | AI Core | N/A |
| affected_software | long text | AI Core | N/A |
| recommended_actions | long text | Specialist | N/A |
| status | single select | Integration | new, processing, analyzed, reviewed |

### IOCs

| Field | Type | Written By | Status Values |
|---|---|---|---|
| ioc_ips | long text | AI Core | N/A |
| ioc_domains | long text | AI Core | N/A |
| ioc_urls | long text | AI Core | N/A |
| ioc_hashes | long text | AI Core | N/A |
| ioc_emails | long text | AI Core | N/A |
| related_threat | linked record | Integration | N/A |

## Conventions

- Use clear folder names by lab or component.
- Keep screenshots in a `screenshots/` folder.
- Keep audit reports in a `docs/` folder.
- Use Markdown files for reports and logs.
- Use JSON files for exported Flowise and n8n workflows.
- Field names should use snake_case when possible.
- Status values should be lowercase.
- Date fields should end in `_at`.
- Boolean fields should start with `is_`.

## Current State

- **What's working:**
  - Flowise LLM chain runner has been created.
  - n8n workflow calls Flowise through HTTP Request nodes.
  - The pipeline successfully classifies, analyzes, and recommends actions for a security alert.
  - GitHub repository contains component folders and Week 8 workflow evidence.

- **What's in progress:**
  - Organizing Week 8 files into a separate folder.
  - Creating Part 2 GitHub Copilot deliverables.
  - Creating audit and prompt log documentation.

- **Known issues:**
  - Some workflow files may contain API keys and should be reviewed before committing to a public repository.
  - The project needs clear documentation for each component.
  - The handoff between all components should be tested end-to-end before Checkpoint 2.

- **Next milestone:** Checkpoint 2 — one record should flow end-to-end through all components without manual intervention.

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
├── DT_Lab_7/
├── screenshots/
└── README.md