# Model Comparison Report — Week 4

**Name:** Ayman Fahim
**Date:** 3/15/2024
**Capstone Project:** AI Summarizer & IOC Extractor
**My Component:** Alert triage/classification and IOC (Indicator of Compromise) extraction

## Test Setup

**Input dataset:** 5 cybersecurity text samples covering:
- 3 clearly concerning/high-severity records (unauthorized login, phishing email, brute-force SSH)
- 1 ambiguous/edge case record (routine firewall update)
- 1 routine/benign record (normal system utilization)

**Models tested:**
1. distilbert-base-uncased-finetuned-sst-2-english (sentiment)
2. facebook/bart-large-mnli (zero-shot classification)
3. dslim/bert-large-NER (named entity recognition)
4. Groq Llama 3.1 8B Instant (LLM classification)

**Evaluation criteria:** label accuracy, confidence score, speed, ease of integration in n8n

## Results Summary

| Record | Sentiment | Zero-Shot | NER Entities | Groq |
|--------|-----------|-----------|-------------|------|
| 1. Unauthorized login from Moscow | NEGATIVE (0.9961) | possible anomaly (0.90) | Moscow (LOC) | HIGH |
| 2. Routine firewall rule update | NEGATIVE (0.9986) | routine activity (1.00) | none | INFORMATIONAL |
| 3. Phishing email (Amazon domain) | NEGATIVE (0.9959) | possible anomaly (0.80) | Amazon (ORG) | HIGH |
| 4. Multiple failed SSH attempts (Beijing) | NEGATIVE (0.9994) | possible anomaly (0.80) | SSH (MISC) | HIGH |
| 5. Normal system resource utilization | NEGATIVE (0.9880) | routine activity (1.00) | none | INFORMATIONAL |

## Analysis

**Where models agreed:** All models correctly identified records 2 and 5 as routine/benign — Zero-Shot labeled both "routine activity" with perfect confidence (1.00), and Groq classified both as INFORMATIONAL. Records 1, 3, and 4 were consistently flagged as threats by both Zero-Shot ("possible anomaly") and Groq (HIGH severity).

**Where models disagreed:** The Sentiment model classified every single record as NEGATIVE, including the two benign ones. This is a clear limitation — it was trained on movie reviews and reads security language as emotionally negative regardless of actual threat level. It cannot distinguish between a routine update and an active attack.

**Most accurate model overall:** Groq Llama 3.1 8B was the most accurate and informative. It correctly differentiated all 5 records, provided severity levels (HIGH vs INFORMATIONAL), and included one sentence of reasoning that would be directly useful in a real security workflow. Zero-Shot was a close second — highly accurate on threat vs. routine classification, though it only offers broad category labels without explanation.

**Fastest/most practical:** Zero-Shot (bart-large-mnli) is the most practical for high-volume use due to its speed and simplicity. Groq is slightly slower but provides richer output. Both are far more useful than Sentiment for this domain.

## Recommended Models for My Capstone Component

**Component:** AI Summarizer & IOC Extractor

**Primary model:** Groq Llama 3.1 8B Instant — best suited for summarizing alerts and generating severity classifications with reasoning, which is the core of the summarizer component.

**Secondary model:** dslim/bert-large-NER — directly supports the IOC extraction component by identifying named entities such as locations (Moscow, Beijing), organizations (Amazon, Cloudflare), and other indicators present in alert text.

**Rejected models and why:**
- distilbert-sst-2 (Sentiment): Every record returned NEGATIVE regardless of actual threat level, making it useless for security triage. It has no concept of cybersecurity severity and cannot distinguish benign from critical alerts.
- facebook/bart-large-mnli (Zero-Shot): Accurate for broad classification but limited to predefined labels and provides no reasoning or summary text. Not suitable as a primary model for a summarizer component, though it could serve as a lightweight pre-filter.

## Failure Cases and Limitations

The most notable failure was the Sentiment model classifying Record 5 ("System resource utilization normal across all monitored hosts — no anomalies detected") as NEGATIVE with 0.9880 confidence. This record is explicitly benign, yet the model flagged it as negative — likely because it was trained on subjective text like movie reviews and treats security language as emotionally negative by default. This tells us that general-purpose NLP models trained on non-domain data should not be used for security triage without fine-tuning. In production, relying on sentiment alone would generate a high false positive rate and erode analyst trust in the system.

A secondary limitation was observed in the NER model for Record 4 — it extracted "SS" (MISC) from "SSH attempts" rather than identifying Beijing as a location. This suggests the model struggled with abbreviations and technical terms, and may require domain-specific fine-tuning or post-processing to reliably extract cybersecurity IOCs like IP addresses, hostnames, and attack vectors.

## Next Steps

With more time, I would test the following:
- Run a larger dataset of 20–50 records to better evaluate false positive and false negative rates across all four models.
- Test a domain-specific NER model fine-tuned on cybersecurity data (e.g., one trained on threat intelligence reports) to improve IOC extraction accuracy.
- Experiment with different Groq system prompts to see if more structured output (e.g., JSON with severity + IOCs + summary) can be generated in a single call, replacing both Groq and NER with one unified LLM step.
- Evaluate Groq with a larger model (llama-3.1-70b) to see if reasoning quality improves for edge cases and ambiguous alerts.

## Reflection

The most surprising finding was how poorly the Sentiment model performed despite its high confidence scores. It labeled every record as NEGATIVE with 98–99% confidence, yet had zero ability to distinguish a critical brute-force attack from a routine maintenance window. This highlighted that confidence scores alone are meaningless without domain relevance — a model can be highly confident and completely wrong for the task. By contrast, Groq demonstrated that a general-purpose LLM with a well-crafted system prompt can outperform specialized smaller models on domain-specific classification tasks, which has significant implications for how I design the summarizer component of my capstone.
