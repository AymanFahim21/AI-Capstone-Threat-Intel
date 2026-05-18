# Component 1: Feed Collector

**Owners:** Mathews and Darius  
**Project:** AI-Capstone-Threat-Intel  
**Component Role:** Ingestion

## What This Component Does

The Feed Collector is the ingestion layer for the AI-Capstone-Threat-Intel project. It collects public cybersecurity threat information from RSS feeds, CVE sources, and public threat feeds, then normalizes each item into a consistent Airtable record that the rest of the system can process.

The goal of this component is to make sure the project always starts with clean, structured threat records. Instead of having each team member manually copy threat articles or CVEs, this workflow creates standardized records with fields such as `title`, `source_name`, `source_url`, `published_at`, `raw_description`, `normalized_text`, and `ai_status`.

## How It Connects to the Other Components

### Inputs

The Feed Collector reads from public threat intelligence sources such as:

- Security blog RSS feeds
- CVE or vulnerability feeds
- Public threat intelligence feeds
- Manual test records for development

### Outputs

The workflow writes records into the Airtable `threats` table. The most important output fields are:

| Field | Purpose |
|-------|---------|
| `title` | Short name of the threat item |
| `source_name` | Where the item came from |
| `source_type` | Type of source: `rss`, `cve`, `threat_feed`, or `manual_test` |
| `source_url` | Link to the original source |
| `published_at` | Original publication date when available |
| `collected_at` | Time the Feed Collector added the record |
| `raw_description` | Original source text or description |
| `normalized_text` | Cleaned text passed to the AI Core |
| `ingestion_status` | Collection status such as `collected`, `duplicate`, or `failed` |
| `ai_status` | Handoff status for AI Core, usually `pending_ai` after collection |
| `last_error` | Error details if collection or normalization fails |

### Handoff to Component 2

After the Feed Collector creates a valid threat record, it should set:

```text
ingestion_status = collected
ai_status = pending_ai
```

The AI Summarizer and IOC Extractor should watch for records where `ai_status` is `pending_ai`, process the `normalized_text`, then write a summary, IOCs, severity, attack type, and confidence back to Airtable.

## Setup Instructions

### Required Accounts and Keys

- n8n Cloud or a local/self-hosted n8n instance
- Airtable account with access to the shared capstone base
- Airtable credential configured in n8n
- Optional: RSS feed URLs, CVE feed URLs, or threat feed URLs selected by the team

### Airtable Setup

Create or confirm the following table before building the workflow:

```text
threats
```

Minimum fields needed for the Feed Collector:

```text
title
source_name
source_type
source_url
published_at
collected_at
raw_description
normalized_text
ingestion_status
ai_status
last_error
```

Recommended status values:

```text
ingestion_status: new, collected, duplicate, failed
ai_status: pending_ai, summarized, ai_failed
```

### n8n Workflow Setup

1. Create a new n8n workflow named `Component 1 — Feed Collector`.
2. Add a trigger node. For early testing, use Manual Trigger. Later, switch to a Schedule Trigger.
3. Add one or more feed source nodes. For RSS, use the RSS Read node or an HTTP Request node that fetches a feed URL.
4. Add a Set/Edit Fields node to normalize the source data into the Airtable field names.
5. Add a duplicate check using `source_url` so the workflow does not create the same record repeatedly.
6. Add an Airtable Create Record node that writes to the `threats` table.
7. Set `ingestion_status` to `collected` and `ai_status` to `pending_ai` for valid records.
8. Add error handling so failed records write a useful `last_error` value.

## How to Test It

### Test 1: Manual Test Record

1. In n8n, run the workflow manually with one test threat item.
2. Confirm that a new Airtable record appears in the `threats` table.
3. Confirm that `title`, `source_url`, `raw_description`, and `normalized_text` are populated.
4. Confirm that `ingestion_status` is `collected`.
5. Confirm that `ai_status` is `pending_ai`.

### Test 2: Duplicate Handling

1. Run the same test item a second time.
2. Confirm that the workflow does not create a second duplicate record.
3. Confirm that the duplicate is skipped or marked with `ingestion_status = duplicate`.

### Test 3: AI Core Handoff

1. Create one clean threat record with `ai_status = pending_ai`.
2. Run the AI Summarizer workflow.
3. Confirm that the same record is updated instead of copied manually.
4. Confirm that AI Core writes summary fields and changes the status to `summarized`.

## Current Status

- The project repository and Feed Collector folder exist.
- Prior lab artifacts show earlier n8n and Airtable work.
- The production Feed Collector workflow still needs to be created for Checkpoint 2.
- The shared Airtable schema needs to be finalized with the team.
- End-to-end handoff from Feed Collector to AI Core has not been confirmed yet.

## Known Limitations

- Public RSS feeds vary in format, so some fields may need fallback logic.
- Some feeds may only provide summaries instead of full article text.
- CVE records and RSS records may require different normalization steps.
- Duplicate detection based only on `source_url` may miss duplicates from different sources covering the same threat.
- The workflow should avoid storing secrets, API keys, or private URLs in exported workflow files.

## Checkpoint 2 Goal

For Checkpoint 2, this component should prove that it can create at least one threat record in Airtable and hand it off automatically to the AI Core by setting `ai_status = pending_ai`.
