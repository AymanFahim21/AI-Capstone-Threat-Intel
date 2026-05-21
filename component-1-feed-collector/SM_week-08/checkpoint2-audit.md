# Prompt Log — Sangram Mathews

**Project:** AI-Capstone-Threat-Intel  
**Team:** AI Capstone Threat Intelligence Team  
**My Component:** AI Core / Threat Intelligence Processing  
**AI Tools Used:** GitHub Copilot, ChatGPT, Groq, n8n, Flowise  

---

## How to Use This Log

This log tracks significant AI-assisted development interactions for the capstone project. It does not include every autocomplete suggestion. It focuses on prompts used to generate, debug, document, or evaluate project work.

---

## 2026-05-20 — Creating Week 8 Copilot project instructions

**Context:**  
I was working in VS Code inside the `AI-Capstone-Threat-Intel` repository. The goal was to complete Week 8 Part 2 by creating `.github/copilot-instructions.md` so GitHub Copilot could understand the project context.

At this point, the project had multiple working pieces:

- A `Threats` Airtable table populated from Krebs RSS and NVD CVE data
- An `AlienVault_OTX` Airtable table populated from AlienVault OTX pulse data
- A `Sources` Airtable table tracking threat intelligence sources
- n8n workflows for collecting Krebs RSS articles, NVD CVEs, and AlienVault OTX pulses
- Workflows for extracting IOCs, creating summaries, assigning severity, detecting attack type, and generating recommended actions
- A relevance scoring workflow that uses Groq to compare threats against a sample technology stack

**Prompt:**

> Using my capstone project context, help me create a `.github/copilot-instructions.md` file for an AI-powered threat intelligence dashboard that uses n8n, Flowise, Airtable, Groq, Hugging Face, AlienVault OTX, NVD CVE data, Krebs RSS feeds, and GitHub.

**Result:**  
The AI generated a structured project instructions file with sections for project overview, architecture, tech stack, Airtable schema, conventions, current state, known issues, and repository structure.

The instructions described the project as an AI-powered threat intelligence dashboard that collects security data from public sources, stores it in Airtable, processes it with n8n and AI workflows, extracts IOCs, summarizes threats, assigns severity levels, and recommends analyst actions.

**Evaluation:**  
The output was useful because it gave Copilot specific context about the project instead of relying on a generic template. It correctly identified that the project uses multiple connected tools: n8n for automation, Airtable for storage, Flowise/Groq for AI processing, and GitHub for documentation.

However, I still needed to review and customize the output because some parts could have been too generic. I needed to make sure the file reflected the actual project updates, including the current Airtable tables and active workflows.

**What I changed:**  
I edited the instructions to include the current project structure and workflow details:

- Added the `Threats`, `Sources`, and `AlienVault_OTX` Airtable tables
- Added current workflow sources: Krebs RSS, NVD CVE API, and AlienVault OTX
- Added AI processing fields such as `Summary`, `Severity Level`, `Attack Type`, `CVE IDs`, `Affected Software`, `IOC IPs`, `IOC Domains`, `IOC URLs`, `IOC Hashes`, `IOC Emails`, `Recommended Actions`, and `Relevance Score`
- Added reminders not to invent API keys, URLs, or Airtable IDs
- Added a warning that sensitive API keys should not be committed to GitHub

**What I learned:**  
AI tools work much better when they have clear project context. The `copilot-instructions.md` file acts like a system prompt for GitHub Copilot, similar to how prompt templates guide Flowise LLM chains. The more accurate the instructions are, the more useful Copilot becomes for writing READMEs, debugging n8n expressions, and documenting workflows.

---

## 2026-05-20 — Auditing the current threat intelligence workflow

**Context:**  
I used AI to review the current state of the capstone project before Checkpoint 2. The project now has multiple working n8n workflows and Airtable tables.

Current project updates include:

- The `Sources` table contains source records for threat intelligence feeds.
- The `Threats` table contains collected Krebs and NVD records.
- The `AlienVault_OTX` table contains OTX pulse records.
- The Krebs RSS workflow collects articles from Krebs on Security and writes new records to Airtable.
- The NVD workflow pulls CVE records from the NVD API and stores them in Airtable.
- The AlienVault OTX workflow collects OTX pulse data and prevents duplicates using `pulse_id`.
- The IOC extraction workflows enrich records with summaries, CVEs, affected software, IOCs, attack type, severity, and recommended actions.
- The relevance scorer workflow uses Groq to score threats against a sample technology stack.

**Prompt:**

> Based on my current Airtable exports and n8n workflows, audit my AI-Capstone-Threat-Intel project for Checkpoint 2 readiness. Tell me what is working, what gaps remain, and what I should fix before submitting.

**Result:**  
The AI identified that the project is partially ready for Checkpoint 2 because the main data flow is now working:

1. Threat data is collected from public sources.
2. Records are normalized and deduplicated.
3. Airtable stores the collected threat records.
4. IOC extraction and summarization enrich the data.
5. Relevance scoring adds an analyst-priority score.

The AI also identified remaining gaps:

- Some workflows are still manually triggered instead of fully automated.
- Some records have `Relevance Score` values still set to `0`.
- Some IOC fields are empty when no indicators are found.
- Some workflow files may contain sensitive API keys and should be cleaned before pushing to GitHub.
- The project needs clearer documentation showing how one record flows end-to-end through all components.

**Evaluation:**  
The audit was helpful because it connected my actual project files to the Checkpoint 2 requirement. It showed that the project has real progress, especially with multiple data sources and enrichment workflows. It also pointed out practical issues that need to be fixed before submission.

The most important issue is that the project needs to clearly prove an end-to-end flow: source collection → Airtable record → AI processing → IOC extraction → relevance scoring → analyst-ready output.

**What I changed:**  
I updated the project documentation to better explain the current workflow. I also planned to add screenshots showing:

- Krebs RSS workflow running successfully
- NVD CVE workflow running successfully
- AlienVault OTX workflow running successfully
- IOC extraction and summarization results
- Airtable records with populated summary, severity, IOCs, and recommended actions
- Relevance score updates

I also noted that API keys should be removed or replaced with placeholders before committing workflow JSON files to GitHub.

**What I learned:**  
A workflow can be technically working, but it still needs documentation and screenshots to prove it works. For Checkpoint 2, it is not enough to have separate workflows. I need to show that the workflows connect into a complete pipeline and that Airtable records move through each processing stage.

---

## 2026-05-20 — Improving IOC extraction and summarization workflows

**Context:**  
I worked on the AI Core part of the project, focusing on extracting indicators of compromise and summarizing threat records. The project includes workflows for Krebs/NVD records and AlienVault OTX records.

The extracted fields include:

- `IOC IPs`
- `IOC Domains`
- `IOC URLs`
- `IOC Hashes`
- `IOC Emails`
- `CVE IDs`
- `Affected Software`
- `Severity Level`
- `Attack Type`
- `Summary`
- `Recommended Actions`

**Prompt:**

> Help me update my n8n workflow so it extracts IOC IPs, domains, URLs, hashes, emails, CVE IDs, affected software, severity, attack type, summaries, and recommended actions from Krebs, NVD, and AlienVault OTX records.

**Result:**  
The AI helped design a deterministic JavaScript extraction approach inside n8n Code nodes. Instead of relying only on Flowise or Groq, the workflow uses regex and structured parsing rules to extract indicators directly from the raw text, CVE descriptions, URLs, and AlienVault OTX indicator arrays.

The workflow now enriches Airtable records with structured security fields and marks records as processed.

**Evaluation:**  
This was useful because deterministic extraction is more predictable than asking an LLM to find every IOC. Regex-based extraction works well for structured indicators such as IP addresses, CVE IDs, URLs, emails, and hashes. For summaries and recommendations, simple logic can create useful first-pass analyst output.

However, the workflow still has limitations. Some domains extracted from article URLs may not be malicious IOCs. Some records do not contain hashes or emails, so those fields remain blank. The workflow also needs validation to separate true malicious indicators from normal reference links.

**What I changed:**  
I used the AI suggestions to improve the n8n Code nodes and Airtable mappings. I also made the workflow update fields such as `AI Processed`, `Summary`, `Severity Level`, `Attack Type`, and `Recommended Actions`.

**What I learned:**  
LLMs are useful for reasoning and summarization, but deterministic code is better for structured extraction tasks. A strong threat intelligence workflow should combine both: rule-based extraction for IOCs and AI-based reasoning for summaries, relevance, and recommendations.

---

## 2026-05-20 — Reviewing relevance scoring with Groq

**Context:**  
I reviewed the relevance scoring workflow for the project. This workflow scores processed threats based on how relevant they are to a sample technology stack.

The sample technology stack used in the workflow is:

- Windows Server 2022
- Python 3.9
- Apache Tomcat
- AWS EC2

The workflow reads processed threat records from Airtable, prepares a Groq prompt, parses the JSON response, and updates the `Relevance Score` field.

**Prompt:**

> Help me evaluate whether my relevance scoring workflow is useful for my threat intelligence dashboard. The workflow uses Groq to compare each threat against my technology stack and returns a score from 0 to 100.

**Result:**  
The AI explained that relevance scoring is useful because it helps prioritize threats that matter most to the organization. For example, a CVE affecting Apache Tomcat or Windows Server should receive a higher score than a threat targeting unrelated software.

The AI also suggested that the scoring prompt should consider:

- Affected software overlap
- Severity level
- CVE presence
- Attack type
- Whether the threat includes actionable indicators
- Whether the source is reliable

**Evaluation:**  
The relevance scoring workflow is a strong addition because it makes the dashboard more analyst-focused. Instead of only collecting threat data, the system helps decide which records deserve attention first.

One issue is that some records still have a score of `0`, so the scoring workflow may need to be rerun or adjusted. Also, the sample tech stack should eventually be replaced with the actual organization’s technology stack.

**What I changed:**  
I documented the current relevance scoring logic and added it to the project explanation. I also noted that future improvements should include configurable technology stacks instead of hardcoded values.

**What I learned:**  
Threat intelligence is more useful when it is connected to the organization’s environment. A vulnerability is not equally important to every organization. Relevance scoring helps turn raw threat data into prioritized security intelligence.

---

## 2026-05-20 — Final Week 8 reflection on AI-assisted development

**Context:**  
I used AI tools to help with Week 8 deliverables, including project instructions, workflow debugging, audit planning, and documentation.

**Prompt:**

> Help me write a reflection explaining how AI-assisted development improved my capstone workflow.

**Result:**  
The AI helped summarize how GitHub Copilot and ChatGPT supported the project by generating documentation, improving prompts, debugging workflow logic, and helping organize the repository.

**Evaluation:**  
The AI output was helpful, but I had to verify it against my actual files. The most useful AI responses were the ones based on real project context, such as Airtable fields and n8n workflow names. Generic AI responses were less useful.

**What I changed:**  
I edited the reflection to mention my actual project updates, including Krebs RSS collection, NVD CVE ingestion, AlienVault OTX enrichment, IOC extraction, summarization, and relevance scoring.

**What I learned:**  
AI-assisted development is most effective when I use it as a project assistant, not as a replacement for understanding the work. I still need to check field names, test workflows, review outputs, and make sure no sensitive keys are committed to GitHub.