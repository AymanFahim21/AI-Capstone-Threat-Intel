# Component 2: AI Summarizer & IOC Extractor
**Owner:** Ayman, Mathews

## Description
Flowise chain that summarizes each threat entry and extracts structured IOCs including affected software, attack type, severity, IP addresses, domains, and file hashes.

## Overview

The **AI Summarizer and IOC Extractor** is the AI Core component of the `AI-Capstone-Threat-Intel` project. This component takes raw threat intelligence records collected from sources such as Krebs on Security, NVD CVE, and AlienVault OTX, then enriches them with analyst-ready fields.

The goal of this component is to turn raw threat data into structured threat intelligence by generating summaries, extracting indicators of compromise, identifying CVEs, assigning severity levels, detecting attack types, and recommending response actions.

This component supports the overall AI threat intelligence dashboard by making collected security data easier to search, prioritize, and investigate.

---

## What This Component Does

This component performs several enrichment tasks:

- Summarizes raw threat intelligence records
- Extracts indicators of compromise, including:
  - IOC IPs
  - IOC domains
  - IOC URLs
  - IOC hashes
  - IOC emails
- Extracts CVE IDs from NVD records and threat reports
- Identifies affected software when available
- Assigns a severity level such as `Low`, `Medium`, `High`, `Critical`, or `Unknown`
- Detects the attack type, such as phishing, malware, ransomware, botnet, credential theft, or vulnerability exploitation
- Generates recommended response actions
- Marks records as AI processed in Airtable
- Supports relevance scoring against a sample technology stack

---

## How It Connects to Other Components

The capstone project is organized into four major components:

| Component | Role | Connection to This Component |
|---|---|---|
| Component 1 — Feed Collector | Collects raw threat data from public sources | Sends new records into Airtable tables such as `Threats` and `AlienVault_OTX` |
| Component 2 — AI Summarizer | Enriches raw records with summaries, IOCs, severity, attack type, and recommendations | Reads unprocessed Airtable records and updates them with structured AI/security fields |
| Component 3 — Relevance Scorer | Scores processed threats based on relevance to a technology stack | Uses enriched summaries and affected software from this component |
| Component 4 — Integration | Connects workflows, dashboard views, and final documentation | Uses enriched Airtable records for reporting and project demonstration |

---

## Data Sources

This component currently supports threat records from:

### Krebs on Security

Krebs RSS articles are collected into the `Threats` table. The enrichment workflow extracts useful information from fields such as title, raw description, raw content, URL, and tags.

### NVD CVE API

NVD CVE records are collected into the `Threats` table. These records usually include CVE IDs, CVSS severity, affected software, descriptions, and NVD URLs.

### AlienVault OTX

AlienVault OTX pulse records are collected into the `AlienVault_OTX` table. The enrichment workflow uses OTX pulse details and structured indicators to extract IPs, domains, URLs, hashes, emails, CVEs, malware families, adversary information, and recommended actions.

---

## Inputs

The component reads records from Airtable.

### Threats Table Inputs

| Field | Description |
|---|---|
| `Threat ID` | Unique threat record identifier |
| `Title` | Threat article title or CVE title |
| `Source` | Source name, such as Krebs on Security or NVD CVE |
| `Source Type` | Type of source, such as RSS or CVE_API |
| `Category` | Threat category, such as Blog or CVE |
| `Published Date` | Date the source published the record |
| `Collected Date` | Date the workflow collected the record |
| `URL` | Link to the original source |
| `Raw Description` | Short raw description from the source |
| `Raw Content` | Full raw content or JSON content |
| `External ID` | External source ID, such as a CVE ID |
| `Dedupe Key` | Unique key used to prevent duplicate records |
| `Processing Status` | Current processing status |
| `Collector Status` | Collection status |
| `AI Processed` | Checkbox or boolean showing whether AI enrichment has been completed |

### AlienVault_OTX Table Inputs

| Field | Description |
|---|---|
| `source` | Source name, usually AlienVault OTX |
| `pulse_id` | Unique OTX pulse ID |
| `title` | OTX pulse title |
| `description` | OTX pulse description |
| `author` | Pulse author |
| `created` | Pulse creation date |
| `modified` | Pulse modified date |
| `tags` | OTX tags |
| `malware_families` | Malware family names if available |
| `industries` | Targeted industries if available |
| `adversary` | Associated adversary if available |
| `references` | External references |
| `TLP` | Traffic Light Protocol value |
| `indicator_count` | Number of indicators in the pulse |
| `AI Processed` | Whether the OTX pulse has already been enriched |

---

## Outputs

After processing, this component updates Airtable with enriched fields.

| Output Field | Description |
|---|---|
| `Summary` | Short analyst-friendly summary of the threat |
| `AI Summary` | AI or workflow-generated summary |
| `Severity Level` | Estimated severity level |
| `Attack Type` | Detected attack type |
| `CVE IDs` | Extracted CVE identifiers |
| `Affected Software` | Software or platforms affected |
| `IOC IPs` | Extracted IP addresses |
| `IOC Domains` | Extracted domains |
| `IOC URLs` | Extracted URLs |
| `IOC Hashes` | Extracted MD5, SHA1, or SHA256 hashes |
| `IOC Emails` | Extracted email indicators |
| `Recommended Actions` | Analyst response recommendations |
| `AI Raw Response` | Notes about how the enrichment was produced |
| `AI Processed` | Set to true after enrichment |
| `Last Processed` | Timestamp of processing |
| `Relevance Score` | Score from 0–100 showing relevance to a sample technology stack |

---

## Current n8n Workflows Used

This component uses the following n8n workflows:

### 1. Krebs and NVD IOC Extractor and Summarizer

This workflow reads new records from the `Threats` table where processing is not complete. It uses JavaScript extraction rules to summarize records and extract IOCs from Krebs and NVD content.

Main tasks:

- Read unprocessed `Threats` records
- Clean raw HTML/text
- Extract URLs, emails, IPs, hashes, CVEs, and domains
- Detect affected software
- Determine severity level
- Detect attack type
- Generate recommended actions
- Update the original Airtable record

### 2. AlienVault OTX — Direct IOC Extractor and Summarizer

This workflow reads unprocessed records from the `AlienVault_OTX` table. It calls the AlienVault OTX API to retrieve full pulse details and structured indicators.

Main tasks:

- Read unprocessed AlienVault OTX records
- Pull full pulse details using `pulse_id`
- Extract structured indicators from OTX
- Extract IPs, domains, URLs, hashes, emails, and CVEs
- Generate a summary
- Assign severity and attack type
- Add recommended actions
- Mark the record as processed

### 3. Krebs and NVD Relevance Scorer

This workflow scores enriched threats based on how relevant they are to a sample technology stack.

Current sample stack:

- Windows Server 2022
- Python 3.9
- Apache Tomcat
- AWS EC2

The workflow uses Groq to return a score from `0` to `100`.

---

## Setup Instructions

### 1. Required Accounts

You need accounts or API access for:

- n8n Cloud
- Airtable
- Groq API
- AlienVault OTX API
- Flowise Cloud, if using Flowise-based LLM chains
- GitHub

---

### 2. Airtable Setup

Create or verify the following Airtable tables:

- `Threats`
- `Sources`
- `AlienVault_OTX`

The `Threats` table should include fields for:

- `Threat ID`
- `Title`
- `Source`
- `Source Type`
- `Category`
- `Published Date`
- `Collected Date`
- `URL`
- `Raw Description`
- `Raw Content`
- `External ID`
- `Dedupe Key`
- `Processing Status`
- `Collector Status`
- `Summary`
- `Severity Level`
- `CVE IDs`
- `Affected Software`
- `Tags`
- `Attack Type`
- `IOC IPs`
- `IOC Domains`
- `IOC URLs`
- `IOC Hashes`
- `IOC Emails`
- `Recommended Actions`
- `AI Processed`
- `Last Processed`
- `Relevance Score`

The `AlienVault_OTX` table should include fields for:

- `source`
- `pulse_id`
- `title`
- `description`
- `author`
- `created`
- `modified`
- `tags`
- `malware_families`
- `industries`
- `adversary`
- `references`
- `TLP`
- `indicator_count`
- `Summary`
- `Severity Level`
- `Attack Type`
- `IOC IPs`
- `IOC Domains`
- `IOC URLs`
- `IOC Hashes`
- `IOC Emails`
- `CVE IDs`
- `Recommended Actions`
- `AI Processed`
- `Last Processed`

---

### 3. n8n Setup

Import the workflow JSON files into n8n:

- `Krebs and NVD IOC Extractor and summarizer.json`
- `AlienVault OTX - Direct IOC Extractor and Summarizer.json`
- `Krebs and NVD Relevance Scorer.json`

Also import the collector workflows if they are not already installed:

- `Feed Collector - Krebs RSS to Airtable - Fixed.json`
- `Feed Collector - NVD CVE to Airtable.json`
- `AlienVault OTX Workflow.json`

After importing, verify:

1. Airtable credentials are connected.
2. Airtable base and table IDs are correct.
3. Field mappings match the current Airtable schema.
4. API keys are stored securely in n8n credentials or environment variables.
5. Workflows are tested manually before enabling automation.

---

### 4. Groq Setup

The relevance scoring workflow uses Groq to compare each threat against a sample technology stack.

Required Groq setup:

1. Create a Groq account.
2. Generate a Groq API key.
3. Store the key securely in n8n credentials or environment variables.
4. Use the model configured in the workflow, such as:

```text
llama-3.3-70b-versatile