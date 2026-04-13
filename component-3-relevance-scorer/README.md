# Component 3: Relevance Scorer
**Owner:** Barry

## Description
This component scores cybersecurity threats based on how relevant they are to the organization's technology stack. The workflow reads enriched threat summaries from Airtable, compares them against technologies listed in the Tech Stack table, sends the data to Groq for analysis, and writes back a relevance score, priority, and explanation.

## Status
## Tools
- n8n
- Airtable
- Groq API

## Input
- Enriched threat summaries from Airtable
- User-defined technology stack from Airtable

## Output
- Relevance score
- Priority level
- Short explanation of why the threat matters

## Demo
The workflow is triggered manually in n8n. It reads the threat records, compares them with the tech stack, and updates Airtable with relevance scores and rankings.
