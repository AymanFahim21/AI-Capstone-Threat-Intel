# Prompt Log — Darius

**Project:** AI-Capstone-Threat-Intel  
**Team:** Mathews, Darius, Ayman, Barry
**My Component:** Feed Collector
**AI Tools Used:** GitHub Copilot, ChatGPT

---

I will add an entry for each significant AI interaction where I intentionally ask an AI tool to generate, explain, review, or debug something for the capstone project. I will not log every autocomplete suggestion. The goal is to track what context I gave the AI, what it produced, whether it was accurate, and what I changed before using it.

---

## 2026-05-17 — Audited Week 8 readiness and created project-specific files

**Context:** I was working on the Week 8 lab for the AI-Capstone-Threat-Intel repository. My component is the Feed Collector, and I had not created the Week 8 Flowise chains or n8n chain pipeline yet. The repository already contained component folders, prior Week 4 and Week 5 lab artifacts, and the Week 3 proposal.

**Prompt:**
> Analyze my Week 8 lab instructions and my group GitHub repository. Assess where I currently am, identify what is missing, and help me create the files and steps needed to complete the lab. My capstone component is Feed Collector, and I have not started the Week 8 workflow yet.

**Result:** The AI identified that the project was not ready for Checkpoint 2 yet because the Week 8 Flowise chains, the n8n pipeline, the Copilot instructions file, the audit report, and prompt log were missing. It helped create a proposed Airtable schema, a `copilot-instructions.md` file, a Checkpoint 2 audit report, a Feed Collector README update, and a Week 8 n8n import template.

**Evaluation:** The result was useful because it gave me a concrete path to finish the lab instead of only summarizing the instructions. I still needed to verify the schema with my team and replace any placeholder names or assumptions before submitting.

**What I changed:** I kept the parts that matched our project, especially the Feed Collector handoff fields. I planned to edit team member names if my instructor expected exact roster names and replace placeholder Flowise URLs with the real endpoints once I created the chatflows.

**What I learned:** Better context produces better AI output. When I included the lab instructions, current repo, project name, and my component, the AI was able to produce project-specific files instead of generic templates.

---

## 2026-05-17 — Debugged Flowise chatflow imports

**Context:** I imported generated Flowise JSON files for the Week 8 chains. The first imports showed outdated node warnings, the Flowise chat box kept loading, and one version returned an error saying the LLM Chain output type was wrong.

**Prompt:**
> The chat box after opening stays loading forever. Recreate the JSON files properly and in a manner where they will work.

**Result:** The AI revised the Flowise files multiple times and eventually generated a version where the output node matched what my Flowise instance expected. It also explained that Flowise expected the LLM Chain output rather than the Output Prediction selector.

**Evaluation:** The first generated files were not compatible with my Flowise version, so I had to provide the actual error messages. Once I included the exact error, the next version worked.

**What I changed:** I deleted the broken imported chatflows and imported the corrected JSON. I also connected my Groq credential manually after import.

**What I learned:** For tool-specific debugging, exact error text matters more than a general description. Screenshots and error messages made the AI response much more useful.

---

## 2026-05-17 — Worked around the two-chatflow Flowise account limit

**Context:** My Flowise account only allowed two chatflows, but the Week 8 lab originally asked for three separate chains: classification, analysis, and recommendation.

**Prompt:**
> I have a problem: Flowise only allows me to have 2 chatflows. How can I work around this for the sake of the APIs in the lab?

**Result:** The AI suggested a single reusable Security Chain Runner that performs different tasks based on labels like `TASK: CLASSIFY`, `TASK: ANALYZE`, and `TASK: RECOMMEND`. It created a Flowise import file and n8n workflow approach using the same Flowise endpoint three times.

**Evaluation:** This was a practical workaround because it kept the same three-stage API logic even though the account could not hold three separate Flowise chatflows. It also gave me a clear explanation I could use if the professor questioned why the same endpoint appeared more than once.

**What I changed:** I used the single runner approach instead of trying to maintain three separate Flowise chatflows.

**What I learned:** A workflow can preserve the required logic even when a platform limitation forces a different implementation. The key is documenting the constraint and showing that the pipeline still performs the required stages.

---

## 2026-05-17 — Fixed n8n HTTP Request syntax and URL placement

**Context:** I pasted my Flowise URL into n8n, but the HTTP Request node returned an `invalid syntax` error. My configuration also mixed up the chatbot URL, prediction URL, and API key fields.

**Prompt:**
> I pasted in the API and this happens. You can see the URL and API here in this screenshot.

**Result:** The AI identified that I had put the Flowise prediction URL in the wrong field and that the n8n JSON body syntax was invalid. It told me to use the `/api/v1/prediction/...` endpoint, clear the API key field unless I had a real key, and use body fields instead of raw JSON to avoid syntax errors.

**Evaluation:** This fixed the workflow. The most important correction was separating the prediction endpoint from the chatbot URL and avoiding fragile raw JSON expressions.

**What I changed:** I corrected the URL field, removed or corrected the Authorization header, and changed the body to send a `question` field with the task label and alert text.

**What I learned:** In n8n, a request can fail even if the external API is fine. Invalid expression syntax inside the node can break the workflow before it even reaches Flowise.

---

## 2026-05-17 — Prepared Week 9 Checkpoint 2 documentation

**Context:** After the Week 8 n8n chain worked, I moved on to Week 9, which requires one record to move through all four capstone components and requires updated documentation, audit report, Copilot instructions, screenshots, and at least five prompt log entries.

**Prompt:**
> Analyze this Week 9 lab file, assess where I currently am, generate any files I need, and guide me to completion.

**Result:** The AI identified that Week 9 is not a standalone lab but a Checkpoint 2 end-to-end integration test. It created a draft `docs/checkpoint2-results.md`, updated `docs/checkpoint2-audit.md`, updated `.github/copilot-instructions.md`, and expanded the prompt log to five entries based on real AI interactions from the lab work.

**Evaluation:** The result is useful as a starting point, but the results file still has to be updated after I actually run the Checkpoint 2 record through Airtable, AI Core, Specialist/Relevance Scorer, and the dashboard.

**What I changed:** I will use the generated test record and screenshot filenames, then replace any `To verify during test run` lines with the actual result after running the pipeline.

**What I learned:** Week 9 is graded more on honest evidence and gap documentation than on pretending the system is perfect. A clear partial/failure report can still be valid if it shows exactly where the integration broke and what the fix plan is.
