# UGR277 Final Project Report  
## AI Threat Intelligence Dashboard - Week 5 Complete Report

**Name:** Saliou Barry  
**Course:** UGR277  
**Project:** AI Threat Intelligence Dashboard  
**Focus Area:** Airtable + n8n + Hugging Face + Model Evaluation

---

# Project Overview

This project focused on building an AI-powered threat intelligence workflow that collects security alerts, analyzes them with machine learning models, and stores results in Airtable. The goal was to compare generic AI models with fine-tuned cybersecurity models and understand how automation tools can be used in real-world security operations.

The system combined:
- Airtable database for storing alerts
- n8n workflow automation
- Hugging Face AI models
- Evaluation metrics for model performance

---

# Part 1: Airtable Setup

An Airtable base was created to store incoming alerts and model predictions.

## Fields Created
- Alert ID
- Timestamp
- Source
- Severity
- Description
- Sentiment
- Confidence
- Processed

## Data Import
Security sample data was imported successfully using CSV files. After fixing field settings, severity values displayed with colored tags:
- LOW = Green
- MEDIUM = Yellow
- HIGH = Orange
- CRITICAL = Red

---

# Part 2: n8n Workflow Automation

An automated workflow was built in n8n to process alerts from Airtable.

## Workflow Steps
1. Search records in Airtable
2. Loop through records
3. Send alert text to AI models
4. Compare outputs
5. Merge results
6. Update Airtable automatically

## Problems Solved
During development, several issues happened:
- Undefined fields
- Wrong mappings
- Empty outputs
- Incorrect expressions
- Airtable update errors

These issues were fixed by adjusting node mappings and expressions.

---

# Part 3: Teachable Machine Model

A phishing vs legitimate image classifier was trained using Teachable Machine.

## Training Setup
- 21 phishing screenshots
- 21 legitimate screenshots
- 10 test images
- Training time: ~30 seconds

## Results
- Accuracy: 80%
- Precision: 80%
- Recall: 80%
- F1 Score: 80%

The model performed well but still missed one phishing sample and flagged one legitimate sample incorrectly.

---

# Part 4: AI Model Comparison

Three models were compared:

## Generic Model
distilbert-base-uncased-finetuned-sst-2-english

## Fine-Tuned Model A
cybersectony/phishing-email-detection-distilbert_v2.4.1

## Fine-Tuned Model B
mrm8488/bert-tiny-finetuned-sms-spam-detection

## Findings

The generic sentiment model gave confident scores but lacked cybersecurity understanding.

The phishing-specific model performed best because it was trained on phishing data.

The spam model was useful but less accurate for phishing detection.

## Best Choice
Fine-Tuned Model A was the best option for the dashboard.

---

# Lessons Learned

This project gave hands-on experience with:

- Workflow automation
- API integration
- Debugging systems
- Machine learning evaluation
- Database management
- Security alert processing

It also showed that task-specific AI models are better than general-purpose models for cybersecurity tasks.

---

# Future Improvements

If this project continues, future upgrades would include:

- Real-time threat feeds
- Custom-trained models
- Better dashboards
- More alert categories
- Live notifications
- Higher accuracy datasets

---

# Conclusion

This project successfully demonstrated how AI, automation, and databases can work together in a cybersecurity environment. Even with troubleshooting challenges, the final system provided valuable experience and practical skills for future security and AI work.
