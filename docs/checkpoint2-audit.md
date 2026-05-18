# Checkpoint 2 Audit — AI-Capstone-Threat-Intel

## Checkpoint 2 Readiness Assessment

### Status: NOT READY

Based on the current repository and my current progress, the project is not ready for Checkpoint 2 yet. The repository has the proposal, component folders, previous Week 4 and Week 5 lab artifacts, and some older n8n workflow exports, but the Week 8 Flowise chains and the Week 8 n8n pipeline have not been created yet. The main Checkpoint 2 requirement is one complete record flowing through all four components end-to-end without manual intervention, and that handoff has not been proven yet.

### What's Working

- The GitHub repository exists and is organized into the expected capstone component folders.
- The project scope is clear: collect public threat intelligence, summarize and extract IOCs, score relevance against a technology stack, and display prioritized results.
- Component 1 has a defined purpose as the Feed Collector.
- Component 2 has a defined purpose as the AI Summarizer and IOC Extractor.
- Component 3 has a defined purpose as the Relevance Scorer.
- Component 4 has a defined purpose as Integration, Testing, and Presentation.
- Prior Week 4 and Week 5 artifacts show that the team has practiced n8n, Airtable, Hugging Face, and Groq workflows.
- A proposed shared Airtable schema now exists in `.github/copilot-instructions.md` so the team has a concrete schema to standardize around.

### Critical Gaps — Must Fix Before Checkpoint 2

- **Build the shared Airtable base.** Owner: Integration lead, with Feed Collector and AI Core support. Create the `threats`, `iocs`, `tech_stack`, `sources`, and `workflow_runs` tables using the exact field names in `.github/copilot-instructions.md`.
- **Build the Week 8 Flowise chains.** Owner: AI Core / Ayman and Mathews. Create `Alert Classifier`, `Threat Analyzer`, and `Response Recommender`, then test that each chain returns valid JSON only.
- **Build the Week 8 n8n pipeline that calls Flowise.** Owner: Feed Collector / Mathews and Darius. Use the import template `n8n_week8_llm_chain_pipeline_template.json`, replace the placeholder Flowise URLs and API key, then verify that all three HTTP Request nodes execute successfully.
- **Define the handoff status values.** Owner: All components. Use `ai_status = pending_ai` after Feed Collector creates a threat, `ai_status = summarized` and `scoring_status = pending_scoring` after AI Core completes, and `scoring_status = scored` after Relevance Scorer completes.
- **Create at least one real end-to-end test record.** Owner: Integration lead. Add one realistic threat record and verify that it moves through ingestion, AI analysis, relevance scoring, and dashboard review without manually copying data between components.
- **Review older workflow field mappings before reuse.** Owner: Component 3 / Barry and Uyi. One older workflow appears to have written `input_text` as a literal formula string, and one field name appears as `generic_score ` with a trailing space. These should not be carried into the shared Airtable base.

### Schema Issues Found

- The repository does not currently include a confirmed shared Airtable schema export. The schema in `.github/copilot-instructions.md` should be treated as the standard unless the team has already created a different shared base.
- Older lab artifacts use fields such as `input_text`, `model_1_sentiment_label`, `model_2_zeroshot_label`, and `model_4_groq_classification`. Those fields are useful for model comparison labs, but they are not enough for the capstone end-to-end threat workflow.
- Component handoffs need explicit status fields. Without `ai_status` and `scoring_status`, the next workflow will not know which records to process.
- The Relevance Scorer should not use field names with trailing spaces. Use `generic_score`, not `generic_score `.
- The project needs consistent severity and priority values. Use lowercase Airtable values: `critical`, `high`, `medium`, `low`, and `info` for severity.

### Recommended Fix Order

1. **Create the Airtable base using the schema in `.github/copilot-instructions.md`.** This should take under 2 hours if the team creates only the needed Checkpoint 2 fields first.
2. **Create the three Flowise chains and test each one manually.** Do not move to n8n until each chain returns clean JSON in Flowise.
3. **Import or manually build the n8n Week 8 chain pipeline.** Replace the placeholder URLs and API key, then run the manual trigger.
4. **Add five clean test records to Airtable.** Use the CSV in `data/week08_threats_import.csv` as a starting point, but only import fields that exist in the Airtable table.
5. **Connect the real capstone handoff.** Feed Collector should write a record with `ai_status = pending_ai`; AI Core should update it to `summarized` and `scoring_status = pending_scoring`; Relevance Scorer should update it to `scored`.
6. **Take all required screenshots.** Capture the three Flowise chains, the n8n pipeline, Copilot working, Copilot instructions, the audit report, and the artifact generation.

### Test Data Gaps

- The project needs normal threat feed records, not just older model-comparison rows.
- The project needs edge cases such as a CVE with no IOC, a very long advisory, a duplicate source URL, and a threat with multiple IOC types.
- The project needs bad-data records to test workflow error handling, such as missing source URL, missing raw description, and invalid published date.
- The project needs at least one record that clearly matches the team technology stack so the Relevance Scorer can prove it prioritizes relevant threats.

### Example Records to Add

- `title`: Outbound DNS beaconing detected from workstation-47; `source_type`: manual_test; `severity expectation`: critical; `IOC`: `evil-domain.example`.
- `title`: Apache HTTP Server CVE advisory affecting reverse proxy deployments; `source_type`: cve; `severity expectation`: high if Apache is in `tech_stack`.
- `title`: Routine firewall maintenance notice; `source_type`: manual_test; `severity expectation`: info or low.
- `title`: Phishing campaign spoofing a cloud storage provider; `source_type`: rss; `severity expectation`: high.
- `title`: Incomplete record missing raw description; expected behavior: Feed Collector or AI Core should mark it failed and write `last_error`.

### My Immediate Next Step

My next step is to create the three Flowise chatflows and confirm that each one returns valid JSON. After that, I will import or rebuild the n8n chain pipeline and replace the placeholder API URLs with my actual Flowise endpoints.
