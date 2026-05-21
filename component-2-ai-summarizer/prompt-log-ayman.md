# Prompt Log — Ayman

**Project:** AI-Capstone-Threat-Intel  
**Team:** Threat Intelligence Feed Dashboard  
**My Component:** Component 2 — AI Summarizer & IOC Extractor  
**AI Tools Used:** GitHub Copilot, ChatGPT, Flowise/Groq-assisted prompt testing

---

## How to Use This Log

This log tracks significant AI-assisted development interactions for the capstone project. Each entry records the context, prompt, result, evaluation, edits made, and what I learned. It does not include ordinary autocomplete suggestions.

---

## 2026-05-21 — Reviewed AI Core role in the Checkpoint 2 pipeline

**Context:** I was checking how Component 2 fits into the Week 9 Checkpoint 2 end-to-end requirement. The system needed to show a record moving from ingestion into AI processing and then into the relevance/dashboard stages.

**Prompt:**
> Using the current AI-Capstone-Threat-Intel repository context, explain what the AI Summarizer & IOC Extractor component is responsible for during Checkpoint 2. Identify its inputs, outputs, and where it hands data off to the next component.

**Result:** The AI described Component 2 as the stage that receives raw or normalized threat records from Airtable, sends the threat text to an LLM/Flowise chain, and writes back structured fields such as summary, severity, attack type, affected software, domains, IP addresses, and other IOCs. It also identified the handoff to the Relevance Scorer as the point where enriched AI fields must be available.

**Evaluation:** The result matched the intended project architecture. It correctly separated the ingestion role from the AI Core role and made clear that Component 2 should not just summarize text; it should create structured outputs that downstream workflows can read.

**What I changed:** I used the explanation to make sure the audit and results report described AI Core as a processing/handoff component, not just a standalone chatbot.

**What I learned:** A component is not checkpoint-ready just because it produces a response. It must write output fields in a predictable format that later workflows can use.

---

## 2026-05-21 — Improved the Flowise/Groq prompt for structured IOC extraction

**Context:** I needed the AI Core chain to return machine-readable threat intelligence instead of a paragraph summary. The output needed to support Airtable updates and relevance scoring.

**Prompt:**
> Create a concise Flowise/Groq system prompt for a threat intelligence AI summarizer. It should take a raw threat description and return JSON only with summary, severity, attack_type, affected_software, indicators, domains, IP addresses, hashes, and confidence. Do not include markdown or extra text.

**Result:** The AI produced a structured prompt that forced JSON-only output and included fields useful for later stages: summary, severity, attack type, affected software, indicators, domains, IP addresses, file hashes, and confidence.

**Evaluation:** The JSON schema was useful, but I had to make sure the field names aligned with the actual Airtable columns and did not introduce names that the workflows would not recognize.

**What I changed:** I kept the JSON-only constraint and adjusted the field names to match the project’s terminology, especially severity, summary, affected software, and indicators.

**What I learned:** Structured output is only useful if the schema matches the database and downstream n8n expressions.

---

## 2026-05-21 — Checked the AI Core handoff fields against Airtable expectations

**Context:** For Checkpoint 2, a record has to move from AI Core to Specialist/Relevance Scorer. I needed to identify which AI-generated fields must be present before scoring can work.

**Prompt:**
> Given a threat intelligence Airtable table with raw title, source, description, URL, AI summary, severity, attack type, affected software, IOCs, and relevance score fields, identify which fields the AI Core should write and which fields the Relevance Scorer should read.

**Result:** The AI separated the table into raw ingestion fields, AI enrichment fields, and scoring fields. It recommended that the AI Core write the summary, severity, attack type, affected software, and IOC fields, while the Relevance Scorer should read those AI fields plus source/title context and then write relevance score, priority, and explanation.

**Evaluation:** This was accurate and helped clarify the handoff boundary. It also exposed a likely integration risk: if the Relevance Scorer expects a field name that differs from what AI Core writes, the end-to-end test will break.

**What I changed:** I documented the field-handoff risk in the Checkpoint 2 materials and treated it as a fix-plan item.

**What I learned:** The most important part of multi-component integration is the contract between components: exact field names, exact status values, and exact expected output formats.

---

## 2026-05-21 — Used AI to prepare a Checkpoint 2 AI Core test case

**Context:** I needed a realistic test record that would clearly exercise the AI summarizer and IOC extractor. The scenario had to contain enough indicators for the AI to extract meaningful fields.

**Prompt:**
> Generate one realistic cybersecurity threat record for an end-to-end integration test. It should involve DNS beaconing or command-and-control behavior and include enough details for an AI summarizer to extract severity, attack type, affected host, domain indicator, and recommended next-stage relevance scoring.

**Result:** The AI suggested a workstation-47 DNS beaconing scenario involving repeated queries to randomized subdomains associated with command-and-control infrastructure.

**Evaluation:** The test case was strong because it was not vague. It contained a host, suspicious behavior, a domain indicator, timing pattern, and expected high-severity classification.

**What I changed:** I used the workstation-47 scenario as the main Checkpoint 2 test record and tied it to the expected path through Ingestion, AI Core, Relevance Scorer, and Dashboard.

**What I learned:** A good test record should be realistic but also deliberately contain evidence that each component can process.

---

## 2026-05-21 — Re-ran the Checkpoint 2 audit from the AI Core perspective

**Context:** After reviewing the local run setup, I needed to update the capstone audit so it reflected the current state instead of the Week 8 state.

**Prompt:**
> Act as a capstone project advisor. Review the AI-Capstone-Threat-Intel project for Checkpoint 2 readiness from the AI Core perspective. Identify what is working, what still needs integration work, schema risks, and the highest-priority fixes before final polish.

**Result:** The AI identified that the project has working AI-processing pieces, including Flowise/Groq and n8n-based summarizer workflows, but that the biggest risk is full automation across all components and consistent updates back to Airtable.

**Evaluation:** The assessment was accurate. It avoided claiming the full pipeline was perfect and treated the checkpoint as a partial but documented integration test.

**What I changed:** I used the audit language to support a PARTIAL Checkpoint 2 status and to explain the need for better automated handoffs between AI Core and downstream scoring/dashboard stages.

**What I learned:** The audit is more useful when it is honest about gaps. A clear partial result is better than overstating that everything works end-to-end.
