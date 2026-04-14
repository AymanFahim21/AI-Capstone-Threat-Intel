## Week 5: AutoML & No-Code Model Training

Trained a custom image classifier with Google Teachable Machine and compared generic vs fine-tuned Hugging Face models for the Threat Classification Engine component of our AI Threat Intelligence Dashboard.

## Custom Model Training
Built a Phishing vs Legitimate Email Screenshot classifier with Google Teachable Machine
Achieved 90% accuracy on 10 held-out test images
Precision: 100% | Recall: 80% | F1: 88.9%

This model helps visually detect phishing email screenshots as part of the threat intelligence pipeline.

## Fine-Tuned Model Comparison

Compared 3 models (1 generic + 2 fine-tuned) on 5 test inputs:

**Generic:** distilbert-base-uncased-finetuned-sst-2-english (Sentiment Analysis)

**Fine-Tuned A:** ealvaradob/bert-finetuned-phishing (Phishing Detection)

**Fine-Tuned B:** openai-community/roberta-base-openai-detector (AI-Generated Text Detection)

Recommended **ealvaradob/bert-finetuned-phishing** for the Threat Classification Engine because it consistently detected phishing content with higher confidence and more relevant labels.

## Fine-tuned models showed higher performance with:

- More relevant classification labels
- Higher confidence scores
- Better handling of security-specific inputs
- Project Component

## Component: Threat Classification Engine

This component:

- Classifies suspicious text inputs
- Detects phishing attempts
- Compares model outputs
- Stores results in Airtable
- Supports AI Threat Intelligence Dashboard

## Tools Used
- Google Teachable Machine
- Hugging Face Models
- n8n Workflow Automation
- Airtable Database

## Workflow Architecture
```
Input Data
    ↓
Generic Model
    ↓
Fine-Tuned Model A
    ↓
Fine-Tuned Model B
    ↓
Merge Results
    ↓
Store in Airtable
```
## Repository Structure
```
week-5/
│
├── report.md
├── README.md
├── screenshots/
└── workflow.json
```
See report.md for full analysis.
