# Capstone Project Context

## Project
- **Name:** AI-Capstone-Threat-Intel
- **Team:** Mathews and Darius — Component 1 Feed Collector; Ayman and Mathews — Component 2 AI Summarizer and IOC Extractor; Uyi and Barry — Component 3 Relevance Scorer; all members — Component 4 Integration, Testing, and Presentation.
- **What it does:** This project builds an automated threat intelligence system that collects cybersecurity threat information from public sources, stores normalized threat records in Airtable, enriches each record with AI-generated summaries and indicators of compromise, and prioritizes threats based on an organization's technology stack. The target users are security analysts and small-to-mid-size IT teams who need a faster way to monitor emerging threats without manually reading every feed item.
- **Project type:** Threat Intelligence Feed Dashboard / Automated Threat Intelligence Hub.

## Architecture
- **Ingestion:** The Feed Collector uses n8n to pull threat intelligence from public RSS feeds, CVE sources, and public threat feeds. It normalizes each item into a common Airtable record with source metadata, title, URL, publication date, raw description, and workflow status fields.
- **AI Core:** The AI Summarizer and IOC Extractor uses Flowise LLM chains with Groq and supporting Hugging Face models to summarize raw threat entries, classify severity, extract attack type, and identify IOCs such as IP addresses, domains, URLs, CVEs, and hashes.
- **Specialist:** The Relevance Scorer uses n8n and Groq to compare enriched threat records against the organization's technology stack in Airtable. It writes relevance scores, priority levels, and short explanations back to the threat record.
- **Integration:** The shared Airtable base acts as the handoff layer between components. Status fields drive each handoff: the Feed Collector creates records, the AI Core processes records marked `pending_ai`, the Relevance Scorer processes records marked `pending_scoring`, and the dashboard uses completed records for analyst review.

## Tech Stack
- n8n Cloud or self-hosted n8n for workflow automation
- Flowise Cloud for LLM chains and API-callable chatflows
- Groq API using `llama-3.3-70b-versatile` for LLM inference
- Hugging Face Inference API for supporting classification / NER experiments
- Airtable for the shared database and dashboard views
- GitHub for repository organization, documentation, workflow exports, prompt logs, and portfolio artifacts
- draw.io for architecture diagrams

## Airtable Schema
This is the target shared schema for Checkpoint 2. Keep field names exact because n8n expressions depend on them.

### threats
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| threat_id | autonumber or formula | Airtable / Integration | N/A |
| title | single line text | Feed Collector | N/A |
| source_name | single select or text | Feed Collector | N/A |
| source_type | single select | Feed Collector | rss, cve, threat_feed, manual_test |
| source_url | URL | Feed Collector | N/A |
| published_at | date/time | Feed Collector | N/A |
| collected_at | date/time | Feed Collector | N/A |
| raw_description | long text | Feed Collector | N/A |
| normalized_text | long text | Feed Collector | N/A |
| ingestion_status | single select | Feed Collector | new, collected, duplicate, failed |
| ai_status | single select | Feed Collector / AI Core | pending_ai, summarized, ai_failed |
| summary | long text | AI Core | N/A |
| attack_type | single select or text | AI Core | phishing, brute_force, malware, c2, vulnerability, misconfiguration, insider_threat, unknown |
| severity | single select | AI Core | critical, high, medium, low, info |
| ai_confidence | number | AI Core | N/A |
| ioc_summary | long text | AI Core | N/A |
| scoring_status | single select | AI Core / Relevance Scorer | pending_scoring, scored, scoring_failed |
| relevance_score | number | Relevance Scorer | 0-100 |
| priority | single select | Relevance Scorer | critical, high, medium, low |
| relevance_explanation | long text | Relevance Scorer | N/A |
| recommended_action | long text | Relevance Scorer / Response Chain | N/A |
| processed_at | date/time | AI Core / Relevance Scorer | N/A |
| last_error | long text | Any workflow | N/A |

### iocs
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| ioc_value | single line text | AI Core | N/A |
| ioc_type | single select | AI Core | ip, domain, url, hash, cve, email, file_path, unknown |
| related_threat | linked record to threats | AI Core | N/A |
| confidence | number | AI Core | 0-1 |
| extracted_by | single select | AI Core | flowise, groq, huggingface, manual |
| created_at | date/time | AI Core | N/A |

### tech_stack
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| technology | single line text | Integration / Relevance Scorer | N/A |
| category | single select | Integration | operating_system, cloud, server, database, language, framework, security_tool, business_app |
| owner | text | Integration | N/A |
| criticality | single select | Integration | critical, high, medium, low |
| is_active | checkbox | Integration | true / false |
| notes | long text | Integration | N/A |

### sources
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| source_name | single line text | Feed Collector | N/A |
| source_type | single select | Feed Collector / Integration | rss, cve, threat_feed |
| feed_url | URL | Feed Collector | N/A |
| is_active | checkbox | Feed Collector | true / false |
| last_checked_at | date/time | Feed Collector | N/A |
| notes | long text | Feed Collector | N/A |

### workflow_runs
| Field | Type | Written By | Status Values |
|-------|------|------------|---------------|
| run_id | single line text | n8n | N/A |
| workflow_name | text | n8n | N/A |
| status | single select | n8n | started, success, failed |
| started_at | date/time | n8n | N/A |
| ended_at | date/time | n8n | N/A |
| records_processed | number | n8n | N/A |
| error_summary | long text | n8n | N/A |

## Conventions
- Field names use `snake_case` exactly.
- Status values are lowercase and use underscores.
- Date fields end in `_at`.
- Boolean fields use the `is_` prefix.
- LLM chain outputs should be valid JSON only, with no markdown fences.
- Severity values should be normalized to lowercase in Airtable even if the LLM returns uppercase.
- n8n workflows should write `last_error` when a node fails or a model response cannot be parsed.
- Public documentation must not include API keys, bearer tokens, Airtable base IDs, or private feed credentials.

## Current State
- **What's working:** The GitHub repository exists with component folders, a Week 3 proposal, an architecture diagram, prior Week 4 model comparison artifacts, and prior Week 5 model comparison/training artifacts. Some n8n workflow exports exist from earlier labs.
- **What's in progress:** Feed source selection, Week 8 Flowise chains, the Week 8 n8n pipeline that calls those chains, and a shared Checkpoint 2 schema.
- **Known issues:** Week 8 Flowise chains are not yet built. The Week 8 n8n chain-calling workflow is not yet built. The shared Airtable base schema is not exported in the repository. Component handoffs have not been proven end-to-end. Component 3 has an older test artifact where `input_text` appears to have been written as a literal formula string, so field mapping should be reviewed before integration. Component 3 also has a `generic_score ` field with a trailing space in one prior workflow export, which should be avoided in the shared schema.
- **Next milestone:** Checkpoint 2 in Week 9 — one complete record should flow from Feed Collector to AI Core to Relevance Scorer to Integration/Dashboard without manual intervention.

## Repository Structure
```text
AI-Capstone-Threat-Intel/
├── .github/
│   └── copilot-instructions.md
├── README.md
├── component-1-feed-collector/
│   ├── README.md
│   ├── SM_week-04-model-comparison/
│   └── SM_week-05-automl-training/
├── component-2-ai-summarizer/
│   ├── README.md
│   ├── week-04-model-comparison/
│   └── week-05-AutoML & No-Code Model Training/
├── component-3-relevance-scorer/
│   ├── README.md
│   └── SB_week-05-automl-trainning/
├── component-4-integration/
│   └── README.md
├── data/
│   ├── README.md
│   └── week08_threats_import.csv
├── docs/
│   ├── Arch diagram.drawio.png
│   ├── proposal.md
│   └── checkpoint2-audit.md
├── screenshots/
└── prompt-log-ren.md
```

## Week 8 LLM Chains
Use the following Flowise chatflows for the Week 8 lab:
1. `Alert Classifier` — classifies raw alert or threat text into severity JSON.
2. `Threat Analyzer` — analyzes classified alerts and identifies attack type, indicators, potential impact, MITRE techniques, and confidence.
3. `Response Recommender` — recommends immediate actions, investigation steps, containment strategy, and escalation decision.

## Guidance for Copilot
When generating documentation or code for this project:
- Use the exact Airtable field names from this file.
- Prefer concrete n8n expressions over generic pseudocode.
- Do not invent API keys, base IDs, table IDs, or private URLs.
- Write deliverables in first person when they are meant to be submitted as my reflection or prompt log.
- For security examples, use documentation-safe IP ranges such as `198.51.100.0/24`, `203.0.113.0/24`, and `192.0.2.0/24`.
