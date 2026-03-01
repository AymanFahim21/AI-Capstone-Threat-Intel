Threat Intelligence Feed Dashboard
Capstone Project Proposal — Week 3
Team Members
Name
Role / Component
GitHub Username
Mathews
Component 1: Feed Collector
Mathews5112
Darius
Component 1: Feed Collector
@placeholder
Ayman
Component 2: AI Summarizer & IOC Extractor
AymanFahim21
Uyi, Barry
Component 3: Relevance Scorer
@placeholder
All members
Component 4: Integration, Testing & Presentation
@placeholder
Problem Statement
Cybersecurity teams are overwhelmed by the volume of threat intelligence published daily across blogs, CVE databases, and public threat feeds — all in different formats. Analysts spend hours manually reading and categorizing this information instead of acting on it. This system automates the collection, summarization, and prioritization of threat data so analysts can focus on the threats that actually matter to their organization.
Target Users
Security analysts and IT administrators at small-to-mid-size organizations who need to stay informed about emerging threats but lack the time or staffing to manually monitor multiple threat intelligence sources daily.
Architecture
See docs/architecture.png in the GitHub repository.
Component Breakdown
Component 1: Feed Collector (Owners: Mathews & Darius)
Description: A scheduled n8n workflow that pulls raw threat data from free public sources including RSS feeds from security blogs, CVE databases, and public threat feeds. Normalizes all entries into a consistent format and stores them in Airtable.
Tools: n8n, Airtable
Input: Raw RSS feed entries, CVE database records, public threat feed data
Output: Normalized threat records stored in the Airtable threats table (title, source, date, raw description, URL)
Standalone demo: Show the n8n workflow running on a schedule, pulling live entries from 2-3 RSS feeds and populating the Airtable threats table in real time
Component 2: AI Summarizer & IOC Extractor (Owner: Ayman)
Description: A Flowise chain that reads each raw threat entry and produces a concise summary, then extracts structured indicators of compromise (IOCs) including affected software, attack type, severity level, and any mentioned IP addresses, domains, or file hashes. An n8n workflow triggers the chain for each new unprocessed entry and writes the structured results back to Airtable.
Tools: Flowise, Groq or Hugging Face API, n8n
Input: Raw threat descriptions from the Airtable threats table (populated by Component 1)
Output: Enriched threat records with AI-generated summaries and extracted IOC fields written back to Airtable; separate linked records in the IOCs table
Standalone demo: Paste a sample threat description into the Flowise chat interface and show it returning a structured summary with extracted IOCs; then show the enriched record appearing in Airtable
Component 3: Relevance Scorer (Owner: Member 4)
Description: An n8n workflow where the user defines their organization's technology stack in an Airtable table (e.g., Windows, Apache, Python). For each enriched threat entry, the workflow sends the threat summary plus the tech stack to Groq, which returns a relevance score and priority ranking. Results are stored back in Airtable.
Tools: n8n, Groq, Airtable
Input: Enriched threat summaries from Airtable (produced by Component 2) and the user-defined tech stack from the tech stack table
Output: Relevance scores and priority rankings added to each threat record in Airtable
Standalone demo: Show a pre-filled tech stack in Airtable, trigger the n8n workflow manually, and show relevance scores appearing on threat records with high-relevance threats ranked at the top
Component 4: Integration, Testing & Presentation (Owner: Member 5)
Description: Designs and builds the shared Airtable base with all tables and linked records. Creates 30+ realistic test threat entries with sample IOCs and a test tech stack. Builds the Airtable dashboard including a prioritized threat feed, IOC search views, severity charts, and weekly briefing summary gallery. Connects all components end-to-end, verifies data flows, writes the README and setup guide, and prepares the final showcase demo and GitHub Pages portfolio page.
Tools: Airtable, GitHub, draw.io
Input: Output from all three other components
Output: Fully integrated system with working dashboard, complete documentation, and a recorded demo walkthrough
Standalone demo: Walk through the Airtable dashboard showing the prioritized threat feed, IOC search, and severity charts using the 30+ test records
Data Sources
Primary data: RSS feeds from public security blogs (e.g., Krebs on Security, SANS ISC), NIST National Vulnerability Database (NVD) CVE feed, public threat intelligence feeds (e.g., AlienVault OTX)
Sample data: 30+ manually created or collected threat entries covering a range of attack types, severity levels, and IOC types for testing and the final demo
Data format: RSS/XML from feeds, JSON from CVE APIs, normalized to a common record format in Airtable
AI Capabilities
Capability
Purpose
Model / API
Text Summarization
Condense long threat descriptions into 2-3 sentence summaries
Groq (LLaMA) via Flowise
IOC Extraction
Pull structured indicators (IPs, domains, file hashes, CVEs) from threat text
Groq (LLaMA) via Flowise
Relevance Scoring
Score each threat against the user's tech stack and assign priority
Groq (LLaMA) via n8n
Text Classification
Categorize threats by attack type and severity
Hugging Face Inference API via n8n
Success Criteria
1. Feed Collector successfully pulls and normalizes entries from at least 3 different public threat sources on a schedule
2. AI Summarizer correctly extracts IOCs (IP, domain, or file hash) from at least 8 out of 10 test threat entries
3. Relevance Scorer assigns higher scores to threats that match the defined tech stack compared to unrelated threats
4. All 5 components integrate correctly and data flows from ingestion through summarization to scoring without manual intervention
5. Airtable dashboard displays a prioritized, filterable threat feed with severity charts and IOC search using the 30+ test records
Timeline
Week
Milestone
3 (Now)
Project proposal + architecture diagram + GitHub repo
4-6
Build individual components, test with sample data
7-9
Add LLM/agent capabilities, refine AI processing
10-12
Integration, error handling, dashboard/UI
13-14
Polish, documentation, demo preparation
15
Final presentation
