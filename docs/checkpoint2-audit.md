# Checkpoint 2 Audit — AI-Capstone-Threat-Intel

## Checkpoint 2 Readiness Assessment

### Status: AT RISK

The project has made progress since Week 8 because the Flowise/n8n API chain is now working. The Flowise account limit was handled by using one reusable task-conditioned Flowise chain runner, and n8n successfully calls that runner three times for classification, analysis, and response recommendation. However, Checkpoint 2 is still at risk until the team proves the real capstone handoff in Airtable: Ingestion must create a record, AI Core must process it automatically, Specialist/Relevance Scorer must act on it, and Integration must show it in the dashboard.

### What's Working

- The GitHub repository is organized into component folders for Feed Collector, AI Summarizer/AI Core, Relevance Scorer, and Integration.
- The capstone project scope is clear: collect public threat intelligence, enrich records with AI, score relevance, and display prioritized threats.
- `.github/copilot-instructions.md` exists in the correct location and contains project-specific context.
- GitHub Copilot is installed and responding inside VS Code.
- Flowise is working with Groq credentials.
- The Flowise account limit was addressed by creating a single reusable Security Chain Runner instead of three separate chatflows.
- n8n successfully calls the Flowise runner in sequence for `TASK: CLASSIFY`, `TASK: ANALYZE`, and `TASK: RECOMMEND`.
- The team now has a proposed Checkpoint 2 test record and screenshot plan.

### Critical Gaps — Must Fix Before Checkpoint 2 Submission

- **Run the real Airtable-based end-to-end test.** Owner: all components. The Week 8 n8n chain proves API calls, but the Checkpoint 2 requirement is one capstone record moving through all four components without manual copying.
- **Capture four Checkpoint 2 stage screenshots.** Owner: submitting student / Integration. Required screenshots should show the record after Ingestion, after AI Core, after Specialist/Relevance Scorer, and in the Integration dashboard.
- **Confirm status field values exactly match between workflows.** Owner: all components. Feed Collector should write `ai_status = pending_ai`; AI Core should write `ai_status = summarized` and `scoring_status = pending_scoring`; Relevance Scorer should write `scoring_status = scored`.
- **Verify shared Airtable field names.** Owner: Integration. n8n expressions will break if Airtable fields use different names, capitalization, or trailing spaces.
- **Update `docs/checkpoint2-results.md` after the actual run.** Owner: submitting student. The results report must describe what happened honestly, including any failure point.
- **Add or verify at least five prompt log entries.** Owner: individual student. The log should include real interactions, what worked, what was wrong, and what changed.

### Schema Issues Found

- The target schema is documented, but the actual Airtable base still needs to be verified against it.
- Older lab workflows used fields from model-comparison exercises that do not fully match the capstone handoff schema.
- Status fields are the highest-risk integration point. The exact values `pending_ai`, `summarized`, `pending_scoring`, and `scored` should be treated as contract values.
- Any field with a trailing space, such as `generic_score `, should be corrected before integration testing.
- Public screenshots and repo files must not expose API keys, bearer tokens, Airtable base IDs, private Flowise URLs, or private feed credentials.

### Recommended Fix Order

1. **Verify the Airtable `threats` table fields.** Confirm the fields listed in `.github/copilot-instructions.md` exist and match exactly.
2. **Create or trigger one clean test record through the Feed Collector.** Use the Checkpoint 2 DNS beaconing test record from `docs/checkpoint2-results.md`.
3. **Watch for AI Core pickup.** Confirm the AI workflow automatically reads the record when `ai_status = pending_ai`.
4. **Watch for Specialist/Relevance Scorer pickup.** Confirm the scorer automatically processes the record when `scoring_status = pending_scoring`.
5. **Open the dashboard view and confirm the final completed record appears.** Filter by the test record title if needed.
6. **Take the four required screenshots and place them in `screenshots/`.** Use the filenames in `docs/checkpoint2-results.md`.
7. **Update `docs/checkpoint2-results.md` with actual outcomes.** Change statuses from `To verify during test run` to `Working`, `Partially Working`, or `Not Working`.

### Test Data Gaps

- The project needs at least one clean manual Checkpoint 2 test record.
- The project should also include edge cases after Checkpoint 2: duplicate source URL, missing raw description, CVE-only advisory with no IOC, and a long advisory with multiple IOCs.
- The project should include at least one record relevant to the technology stack so the Relevance Scorer can demonstrate prioritization.

### Immediate Next Step

Run the test record in `docs/checkpoint2-results.md` through the real Airtable/n8n/Flowise process, then update the results file with screenshots and actual component statuses.
