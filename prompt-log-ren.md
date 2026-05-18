# Prompt Log — Ren

**Project:** AI-Capstone-Threat-Intel  
**Team:** Mathews, Darius, Ayman, Uyi, Barry, and Integration/Presentation members  
**My Component:** Feed Collector / Ingestion  
**AI Tools Used:** GitHub Copilot, ChatGPT

---

## How to Use This Log

I will add an entry for each significant AI interaction where I intentionally ask an AI tool to generate, explain, review, or debug something for the capstone project. I will not log every autocomplete suggestion. The goal is to track what context I gave the AI, what it produced, whether it was accurate, and what I changed before using it.

---

## 2026-05-17 — Audited current Checkpoint 2 readiness

**Context:** I was working on the Week 8 lab for the AI-Capstone-Threat-Intel repository. My component is the Feed Collector, and I had not created the Week 8 Flowise chains or n8n chain pipeline yet. The repository already contained component folders, prior Week 4 and Week 5 lab artifacts, and the Week 3 proposal.

**Prompt:**
> Analyze my Week 8 lab instructions and my group GitHub repository. Assess where I currently am, identify what is missing, and help me create the files and steps needed to complete the lab. My capstone component is Feed Collector, and I have not started the Week 8 workflow yet.

**Result:** The AI identified that the project is not ready for Checkpoint 2 yet because the Week 8 Flowise chains, the n8n pipeline, the Copilot instructions file, the audit report, and prompt log were missing. It helped create a proposed Airtable schema, a `copilot-instructions.md` file, a Checkpoint 2 audit report, a Feed Collector README update, and a Week 8 n8n import template.

**Evaluation:** The result was useful because it gave me a concrete path to finish the lab instead of only summarizing the instructions. I still need to verify the schema with my team and replace any placeholder names or assumptions before submitting.

**What I changed:** I kept the parts that match our project, especially the Feed Collector handoff fields. I need to edit team member names if my instructor expects exact roster names and replace placeholder Flowise URLs with the real endpoints once I create the chatflows.

**What I learned:** Better context produces better AI output. When I included the lab instructions, current repo, project name, and my component, the AI was able to produce project-specific files instead of generic templates.
