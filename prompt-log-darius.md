# Prompt Log — Darius

**Project:** AI-Capstone-Threat-Intel  
**Team:** AI-Capstone-Threat-Intel  
**My Component:** Feed Collector / Ingestion with Integration support  
**AI Tools Used:** ChatGPT, GitHub Copilot  

---

## How I Use This Log

This log tracks significant AI-assisted development interactions for the capstone project. I am not logging every autocomplete or minor wording change. I am logging cases where I used AI to understand requirements, design implementation logic, debug workflow behavior, create project documentation, or evaluate the quality of the working system.

---

## 2026-05-15 — Debugging the Week 4 Airtable / n8n field mismatch

**Context:** I was working on the Week 4 n8n workflow and the Airtable Search Records node failed with an invalid filter formula. The error said Airtable did not recognize `input_text`, even though I believed the field existed.

**Prompt:**
> in search records: (input_text is actually named correctly in airtable) Here is the error: { "errorMessage": "Your request is invalid or could not be processed by the service", "errorDescription": "The formula for filtering records is invalid: Unknown field names: input_text" }

**Result:** The AI helped diagnose that Airtable formula field names must match the actual field name exactly and that the workflow could be pointing to the wrong table, view, or renamed field. It guided me to check the Airtable schema, verify the field in the exact table being queried, and adjust the filter expression.

**Evaluation:** This was useful because the workflow error looked like an n8n issue at first, but the real problem was the Airtable schema/formula relationship.

**What I changed:** I verified the table and field naming directly in Airtable, then adjusted the workflow configuration so the Search Records node matched the real schema.

**What I learned:** In n8n + Airtable workflows, exact field names and table selection matter more than assumptions. A workflow can execute successfully overall even when a later branch or lookup is not doing what I expected.

---

## 2026-05-15 — Rewriting the Week 4 report around my actual capstone project

**Context:** After the Week 4 workflow ran, I needed the report to be written specifically for my capstone instead of sounding generic.

**Prompt:**
> completely remake report.md with this information: my capstone project is "AI-Capstone-Threat-Intel" quick description: The project builds an automated threat intelligence system that collects, analyzes, and prioritizes cybersecurity threats from public sources.

**Result:** The AI rewrote the report around the project name, project purpose, n8n workflow, Airtable records, and how the lab connected to public-source threat intelligence.

**Evaluation:** This was helpful because the documentation became specific to the capstone instead of describing a disconnected classroom exercise.

**What I changed:** I reviewed the generated wording and kept the sections that matched the actual workflow behavior.

**What I learned:** AI-generated reports are most useful when I provide the project name, project purpose, and the exact result I observed in the tool.

---

## 2026-05-16 — Planning the Week 5 AutoML and model-comparison lab

**Context:** I had not started the Week 5 lab and needed to understand the workflow, Teachable Machine section, n8n comparison workflow, Airtable results, and final files.

**Prompt:**
> Analyze these files, assess where I currently am and help me finish this lab. If any files are required, generate me the file I need to import/use and guide me to completion. Let me know what my next steps are. I currently do not have the workflow created nor have I really started on this lab. If there is any information from me that will help you in completing this lab (like capstone info or anything else), inform me in your response and I will update you.

**Result:** The AI broke the lab into setup steps, workflow steps, Teachable Machine requirements, Airtable exports, and final GitHub deliverables.

**Evaluation:** This was useful because the lab had multiple parts and I needed an ordered plan rather than a general explanation.

**What I changed:** I followed the plan but still handled the live tool setup manually because the AI could not operate Teachable Machine, Airtable, or n8n directly.

**What I learned:** For labs with several tools, the best AI prompt is one that asks for current-state assessment, required files, manual steps, and final submission structure.

---

## 2026-05-16 — Building the Week 5 results package from the workbook and Airtable CSV

**Context:** I had completed the Teachable Machine and Airtable portions and uploaded the result workbook and Airtable CSV. I needed the metrics and final report generated.

**Prompt:**
> here is the result workbook and the airtable csv. Calculate all of the results and create that report, readme, and whatever else I need

**Result:** The AI analyzed the result files, calculated the required comparison results, and generated the Week 5 report/readme structure for GitHub submission.

**Evaluation:** This was effective because the calculations and written analysis were grounded in the exported data instead of guesses.

**What I changed:** I reviewed the metrics and made sure the report matched the evidence from my actual result workbook and Airtable CSV.

**What I learned:** Uploading the actual export files lets AI produce much more accurate lab documentation than describing the results manually.

---

## 2026-05-17 — Starting the Feed Collector RAG / Flowise lab

**Context:** I had not created the Flowise workflow yet. My capstone component was the Feed Collector, so I needed the lab adapted to that component.

**Prompt:**
> Analyze these files, assess where I currently am and help me finish this lab. If any files are required, generate me the file I need to import/use and guide me to completion. Let me know what my next steps are. I currently do not have the workflow created nor have I really started on this lab. There is extra information that must be given: My Capstone Component is "Feed Collector".

**Result:** The AI connected the lab instructions to my Feed Collector role and explained how to build the Flowise/RAG assistant around documents describing collection, normalization, deduplication, source reliability, rate limits, and repeated runs.

**Evaluation:** This helped because the lab was easier to complete once the RAG assistant had a clear purpose inside the larger capstone.

**What I changed:** I used the Feed Collector as the domain focus rather than treating the chatbot as a generic Q&A system.

**What I learned:** RAG quality depends heavily on giving the assistant the right project-specific knowledge base.

---

## 2026-05-17 — Completing the Week 7 chatbot report from test history

**Context:** I had the AI chatbot history showing the example messages and needed the final report and repo structure.

**Prompt:**
> Here is the ai chatbot history showing all of the example messages. If this is all you need, Complete the report for me. Then, tell me exactly how to structure my github repo and do not have it contain anything that I don't need to submit, and write everything as though it was authored by me.

**Result:** The AI produced a completed report using the actual chatbot tests. The report covered document-grounded answers, edge cases, settings experiments, and a reflection on how RAG connects to the Feed Collector.

**Evaluation:** This worked well because the report was based on real interactions with the chatbot rather than a hypothetical description.

**What I changed:** I kept the repo structure limited to what the lab required and avoided unnecessary files.

**What I learned:** For submission work, asking AI to avoid extra files is important because a cluttered repo can make the deliverable harder to grade.

---

## 2026-05-17 — Creating the Week 8 capstone audit and AI-assisted development artifacts

**Context:** Week 8 introduced the prompt log and capstone audit. I needed to connect the audit to the current state of the capstone project and prepare artifacts for Checkpoint 2.

**Prompt:**
> Analyze this file, assess where I currently am and help me finish this lab. If any files are required, generate me the file I need to import/use and guide me to the completion.

**Result:** The AI translated the Week 8 lab into capstone-specific deliverables: audit report, Copilot instructions, prompt log, screenshots, and a plan for improving the pipeline before Checkpoint 2.

**Evaluation:** This was useful because Week 8 was less about building a separate project and more about documenting readiness, gaps, and how AI-assisted development was being used.

**What I changed:** I tied the audit to the real capstone stack: n8n, Flowise, Airtable, public threat feeds, relevance scoring, and dashboard review.

**What I learned:** A capstone audit is only useful if it describes the current system honestly rather than pretending every component is finished.

---

## 2026-05-18 — Using the local run setup to complete Week 9 / Checkpoint 2

**Context:** For Week 9, I needed to use the Local Run Setup and the current capstone repository files to complete Checkpoint 2. The goal was to document an end-to-end pipeline run and update the audit and Copilot artifacts.

**Prompt:**
> I think you misunderstood. Look at the "Local Run Setup" and with this information, week-9, (which is lab 8) entirely, then guide me on submission.

**Result:** The AI reframed the assignment around the local run setup and Week 9 requirements. It identified the files needed for submission, including `docs/checkpoint2-results.md`, `docs/checkpoint2-audit.md`, `.github/copilot-instructions.md`, screenshots, and the prompt log.

**Evaluation:** This was important because my first request was misunderstood. Refining the prompt corrected the scope and produced a more accurate Week 9 plan.

**What I changed:** I redirected the AI to use the Local Run Setup as the source of truth and to focus specifically on Week 9/Checkpoint 2.

**What I learned:** When the AI misunderstands the lab number or context, the fastest fix is to restate the exact source it should use and the exact week/lab mapping.

---

## 2026-05-18 — Clarifying the Week 9 submission checklist and repository target

**Context:** I needed to know exactly what to commit and where to commit it.

**Prompt:**
> What is the full submission checklist from the pdf? What repo do I commit the files to? Is there anything else?

**Result:** The AI extracted the Week 9 checklist and confirmed that the files should go into the capstone repository rather than a separate lab repository.

**Evaluation:** This was useful because it prevented me from scattering deliverables across the wrong repo or adding unnecessary files.

**What I changed:** I used the capstone repo as the target and checked the file paths before committing.

**What I learned:** For project-based labs, the repo destination matters as much as the file content.

---

## 2026-05-18 — Updating Week 9 artifacts for team submission alignment

**Context:** After uploading the required Week 9 files to the capstone repo, I needed additional files for group members Ayman and Matthews to submit.

**Prompt:**
> Now, generate me the files that group members Ayman and Matthews need to submit. These are the only files I've uploaded for this week to the capstone repo: .github/copilot-instructions.md, docs/checkpoint2-results.md, docs/checkpoint2-audit.md, screenshots/, prompt-log-{myname}.md

**Result:** The AI generated role-appropriate submission files based on the shared capstone artifacts already in the repo.

**Evaluation:** This helped align the team submission while keeping each member's work tied to the same project evidence.

**What I changed:** I treated the shared repo artifacts as common evidence and kept the individual prompt logs separate.

**What I learned:** In a team capstone, shared artifacts and individual artifacts need to be clearly separated so nobody overwrites another person’s work.

---

## 2026-05-18 — Explaining the relevance scorer for presentation

**Context:** The relevance scorer was my presentation focus. I needed to understand how it worked, how it connected to the rest of the capstone, and how to explain it clearly.

**Prompt:**
> Completely explain the ins and outs of the relevancy scorer. This is the part I will be presenting. Make sure to explain its connection to the other parts of the project and how they all fit together.

**Result:** The AI explained the relevance scorer as the prioritization layer that converts collected threat intelligence into scored, sortable records for downstream review and dashboard display.

**Evaluation:** This was helpful because it connected my component to the full system instead of treating the scorer as an isolated workflow.

**What I changed:** I focused my explanation on inputs, scoring criteria, routing/output fields, and dashboard impact.

**What I learned:** A good technical presentation should explain not only what a component does, but what decision it enables in the larger pipeline.

---

## 2026-05-18 — Explaining the n8n relevance scorer workflow nodes and Q&A

**Context:** I uploaded the AlienVault OTX and Krebs/NVD relevance scorer JSON workflows and needed a node-by-node explanation plus likely questions.

**Prompt:**
> Explain each node in these jsons, explain relevance scorers, and everything i need to say about it. At the end, add a Q&A.

**Result:** The AI broke down the workflow nodes, explained how scores are calculated and passed through the system, and generated a Q&A section for presentation prep.

**Evaluation:** This was useful because n8n workflows can look complex visually. A node-by-node explanation helped me understand and explain the automation path.

**What I changed:** I used the explanation to prepare a simpler verbal summary focused on source ingestion, score parsing, Airtable update, and dashboard visibility.

**What I learned:** Complex workflows are easier to present when each node is explained by purpose, input, output, and failure mode.

---

## 2026-05-21 — Interpreting the Week 10 Phase 4 requirements

**Context:** I was working on the final lab for the AI-Capstone-Threat-Intel project. The project pipeline was already working end-to-end, and the Streamlit dashboard was live. I needed to translate the Week 10 lab instructions into the exact files, screenshots, and manual actions required for submission.

**Prompt:**
> This is the last lab. Look through previous chats in this project, and complete this entire lab for me. Explain the list of everything I must do manually if needed, and what files to submit. Generate the files I need if possible. Know that the project is complete and fully working, with streamlit fully live. the working link to the dashboard: https://ai-capstone-threat-intelligence-dashboard.streamlit.app/

**Result:** The AI broke the lab into four deliverable categories: error handling, routing logic, dashboard views, and prompt log update. It connected the generic assignment requirements to my actual capstone project by treating the Feed Collector as the ingestion component and the relevance scorer as the equivalent of confidence-based routing.

**Evaluation:** This was useful because the lab instructions were broad and role-based. The AI helped convert them into a project-specific checklist instead of a generic description.

**What I changed:** I kept the project-specific framing but planned to verify each screenshot manually in n8n, Airtable, and Streamlit before submitting.

**What I learned:** For capstone labs, AI is most useful when I provide the current state of the project and ask for a deliverable-level checklist rather than asking only for a summary of the PDF.

---

## 2026-05-21 — Designing the ingestion error handling path

**Context:** I needed the Feed Collector / Ingestion workflow to handle malformed threat-intelligence records instead of dropping them. The system collects public threat intelligence and stores it for later extraction, scoring, and dashboard review.

**Prompt:**
> Help me add error handling to my n8n ingestion workflow for threat intelligence records. I need to validate required fields and write bad records to Airtable with status = error and error_reason populated.

**Result:** The AI suggested adding an IF or validation branch before the scoring path. Required fields should include source/feed source, a title or summary, and an actionable indicator such as IOC, CVE, indicator, or URL. The false path should set `status = error` and write a specific `error_reason` to Airtable.

**Evaluation:** The suggestion matched the Week 10 requirement because the record is not silently dropped and can be seen later in Airtable or the dashboard.

**What I changed:** I adapted the validation to the actual field names in the Airtable base and workflow JSON. I also made the error reason specific enough for debugging.

**What I learned:** Error handling is not just about preventing crashes. For this project, the key is preserving failed records with enough context to retry or fix them.

---

## 2026-05-21 — Choosing relevance-score routing as the confidence equivalent

**Context:** The lab asks for confidence-based routing, but my capstone pipeline uses relevance scoring to prioritize threat intelligence instead of a simple model confidence score.

**Prompt:**
> My project does not use a generic confidence field. It uses a relevance_score from the threat intelligence scorer. What is the best equivalent routing logic for the Week 10 lab?

**Result:** The AI recommended using `relevance_score >= 70` as the automatic analyzed path and `relevance_score < 70` as the human review path. High-relevance items become `analyzed`; low or borderline items become `needs_review`.

**Evaluation:** This worked because it satisfies the “equivalent routing logic” option in the lab and matches the project’s actual purpose: prioritizing actionable threat intelligence.

**What I changed:** I used a threshold of 70 instead of 80 because relevance scoring is broader than pure model confidence. A score of 70 still captures useful threat intelligence without automatically promoting low-value articles.

**What I learned:** When an assignment uses generic AI terminology, I can map it to the closest real decision point in my system as long as I explain the mapping clearly.

---

## 2026-05-21 — Generating test records for both routing paths

**Context:** The lab requires evidence that at least one record goes down each routing path. I needed safe test records that would clearly trigger `analyzed`, `needs_review`, and `error` states.

**Prompt:**
> Generate realistic threat intelligence test records for Week 10: one malformed record for the error path, one high relevance record for analyzed, and one low relevance record for needs_review.

**Result:** The AI generated a CSV-style set of test records with source, feed type, title, summary, IOC or CVE values, URL, relevance score, expected status, and notes.

**Evaluation:** The records are useful because they are intentionally simple and easy to verify in Airtable. They are not random placeholders; each record tests a specific route.

**What I changed:** I planned to adjust field names during Airtable import if my existing table uses different names.

**What I learned:** Test records are better when each one has one clear purpose. That makes screenshots easier to explain in the submission.

---

## 2026-05-21 — Writing dashboard view descriptions

**Context:** The Streamlit dashboard is live, and the lab requires at least two dashboard views with one sentence explaining each view and who it is for.

**Prompt:**
> Write concise dashboard view descriptions for pipeline status, error monitor, and component activity for my threat intelligence dashboard.

**Result:** The AI produced three view descriptions: Pipeline Status for the team, Error Monitor for debugging failed records, and Component Activity for explaining the end-to-end flow to a new viewer.

**Evaluation:** The descriptions are concise and directly aligned with the rubric. They explain both what the view shows and who uses it.

**What I changed:** I added the live Streamlit dashboard link and kept the descriptions focused on status, error_reason, created time, source, and relevance score.

**What I learned:** Dashboard explanations should not just describe the interface. They should describe the operational purpose of each view.

---

## 2026-05-21 — Building the final Week 10 submission package

**Context:** I needed the final lab files organized so they could be committed to the capstone GitHub repository with the screenshots.

**Prompt:**
> Generate the files I need for Week 10 and tell me exactly what must be done manually before submission.

**Result:** The AI created a Week 10 report draft, this prompt log, a manual implementation guide, a test records CSV, and a submission structure checklist.

**Evaluation:** The generated files saved time and gave the submission a clear structure. The AI could not take real screenshots from n8n, Airtable, or the live dashboard, so those still need to be completed manually.

**What I changed:** I will review the generated files before committing them and replace any screenshot placeholder references with actual screenshots from my working project.

**What I learned:** AI can generate most documentation, but final evidence still has to come from the actual running system.

---

## 2026-05-21 — Creating a precise Week 10 screenshot guide

**Context:** After generating the Week 10 files, I still needed exact directions for where to take each screenshot and what each image should prove.

**Prompt:**
> Give me a guide on where exactly to take these screenshots. For each screenshot, tell me exactly what I need to do and show.

**Result:** The AI created a screenshot-by-screenshot guide explaining where to go in n8n, Airtable, and Streamlit; what to click; what fields/nodes must be visible; and what filenames to use.

**Evaluation:** This was useful because the assignment requires evidence, and vague screenshots could lose points even if the underlying project works.

**What I changed:** I will take the screenshots manually from the live tools and save them using the exact filenames referenced in the submission document.

**What I learned:** A screenshot should prove a specific claim. For this lab, each screenshot needs to show either routing logic, error handling, or dashboard visibility.

---

## 2026-05-21 — Merging prompt log entries so the GitHub file does not overwrite older work

**Context:** I noticed that uploading a new `prompt-log-darius.md` could overwrite previous entries in GitHub. I needed one cumulative prompt log instead of a Week 10-only file.

**Prompt:**
> Also, I noticed that the prompt log does not include the logs from previous labs. Look through the previous prompt logs that you generated and create the prompt log that includes everything. Because whenever I upload the new prompt log, I'm pretty sure it overwrites the old one on github.

**Result:** The AI regenerated the prompt log as a cumulative file with entries from the earlier capstone labs, the Checkpoint 2 work, the relevance-scorer work, and the Week 10 final lab.

**Evaluation:** This fixed the overwrite problem by making the root `prompt-log-darius.md` the single complete file to commit.

**What I changed:** I will replace the old GitHub prompt log with this cumulative version instead of uploading a separate Week 10-only prompt log.

**What I learned:** For files that are repeatedly updated across labs, the safest workflow is to append to the existing file and commit the complete current version each time.
