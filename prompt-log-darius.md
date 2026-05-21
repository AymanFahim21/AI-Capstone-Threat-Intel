# Prompt Log — Darius

**Project:** AI-Capstone-Threat-Intel  
**Team:** Mathews, Darius, Ayman
**My Component:** Feed Collector / Ingestion  
**AI Tools Used:** GitHub Copilot, ChatGPT

---

## How to Use This Log

I will add an entry for each significant AI interaction where I intentionally ask an AI tool to generate, explain, review, or debug something for the capstone project. I will not log every autocomplete suggestion. The goal is to track what context I gave the AI, what it produced, whether it was accurate, and what I changed before using it.

---

## 2026-05-17 — Audited Week 8 readiness and created project-specific files

**Context:** I was working on the Week 8 lab for the AI-Capstone-Threat-Intel repository. My component is the Feed Collector, and I had not created the Week 8 Flowise chains or n8n chain pipeline yet. The repository already contained component folders, prior Week 4 and Week 5 lab artifacts, and the Week 3 proposal.

**Prompt:**
> Analyze my Week 8 lab instructions and my group GitHub repository. Assess where I currently am, identify what is missing, and help me create the files and steps needed to complete the lab. My capstone component is Feed Collector, and I have not started the Week 8 workflow yet.

**Result:** The AI identified that the project was missing the Week 8 Flowise chains, the n8n pipeline, the Copilot instructions file, the audit report, and the prompt log. It helped create project-specific files and a proposed submission structure.

**Evaluation:** The result was useful because it gave me a concrete path instead of only summarizing the instructions. I still needed to verify project-specific assumptions with the actual local setup.

**What I changed:** I kept the parts that matched our threat intelligence project and replaced generic assumptions with the actual local run workflows and dashboard details.

**What I learned:** AI output is much better when the prompt includes the lab instructions, the repo context, the project name, and my component.

---

## 2026-05-17 — Debugged Flowise chatflow imports

**Context:** I imported Flowise JSON files for the Week 8 chains. The first versions caused outdated node warnings, the chat box kept loading, and one version returned an output-type error.

**Prompt:**
> The chat box after opening stays loading forever. Recreate the JSON files properly and in a manner where they will work.

**Result:** The AI revised the Flowise JSON files and eventually produced a compatible version where the output node matched my Flowise instance.

**Evaluation:** The first generated files were not compatible with my Flowise version, but providing the exact error message made the next response useful.

**What I changed:** I deleted the broken imported flows, imported the corrected JSON, and connected my Groq credential manually.

**What I learned:** Exact error messages and screenshots are critical when debugging platform-specific workflow tools.

---

## 2026-05-17 — Worked around the two-chatflow Flowise account limit

**Context:** Flowise only allowed me to have two chatflows, while the lab wanted three stages: classification, analysis, and recommendation.

**Prompt:**
> I have a problem: Flowise only allows me to have 2 chatflows. How can I work around this for the sake of the APIs in the lab?

**Result:** The AI suggested a single task-conditioned Security Chain Runner that performs `TASK: CLASSIFY`, `TASK: ANALYZE`, and `TASK: RECOMMEND` depending on the prompt sent by n8n.

**Evaluation:** This was practical because it preserved the three-stage API logic even though the account limit prevented three separate Flowise chatflows.

**What I changed:** I used the single runner approach and called the same endpoint three times from n8n with different task labels.

**What I learned:** A documented workaround can still satisfy the technical purpose of a lab when a platform limitation prevents the exact original implementation.

---

## 2026-05-17 — Fixed n8n HTTP Request syntax and URL placement

**Context:** I pasted the Flowise URL into n8n, but the HTTP Request node failed because I mixed up the chatbot URL, prediction URL, and API key field.

**Prompt:**
> I pasted in the API and this happens. You can see the URL and API here in this screenshot.

**Result:** The AI identified that the Flowise prediction URL needed to go in the URL field and that the API key field should be blank unless I had a real key. It also recommended using body fields instead of raw JSON to avoid invalid expression syntax.

**Evaluation:** This fixed the n8n chain.

**What I changed:** I corrected the URL field, removed incorrect Authorization header values, and sent a `question` field containing the task label and alert text.

**What I learned:** n8n can fail before contacting the API if its internal expression syntax is invalid.

---

## 2026-05-18 — Used the Local Run Setup to document Checkpoint 2

**Context:** The project had a local run setup with five n8n workflows, three Airtable CSV exports, and a Streamlit dashboard. I needed to complete Week 9 / Lab 8 as a Checkpoint 2 integration submission.

**Prompt:**
> Look at the Local Run Setup and with this information, complete Week 9, which is Lab 8, entirely, then guide me on submission.

**Result:** The AI converted the local run information into Week 9 deliverables: `docs/checkpoint2-results.md`, `docs/checkpoint2-audit.md`, updated `.github/copilot-instructions.md`, this prompt log, and a local-run submission guide.

**Evaluation:** The result was useful because it matched the real state of the project instead of pretending the system was fully productionized. It labeled the result as partial integration and listed the exact screenshots still needed from my live tools.

**What I changed:** I kept the honest `PARTIAL` status because the current system has working stages but not one fully automated master handoff.

**What I learned:** For Checkpoint 2, honest documentation of what works and what breaks is more defensible than claiming a perfect end-to-end pipeline when the project is still source-specific and locally configured.
