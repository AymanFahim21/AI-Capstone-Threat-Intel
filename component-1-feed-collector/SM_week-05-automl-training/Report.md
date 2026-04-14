# Week 5 Report: AutoML Training & Fine-Tuned Model Evaluation

**Name:** Sangram Mathews

**Date:** April 13, 2026

**Capstone Project:** AI Threat Intelligence Dashboard

**My Component:** Feed Collector (Threat Classification & Model Evaluation)

## Part A: Teachable Machine Training
### Training Setup
- **Task:** Phishing vs Legitimate Email Screenshot Classification
- **Training images per class:** 25 phishing / 25 legitimate
- **Test images per class:** 5 phishing / 5 legitimate
- **Total training time:** ~30 seconds
```### Test Results
| # | Actual Class | Predicted Class | Confidence | Correct? |
|---|--------------|-----------------|------------|----------|
| 1 | Phishing     | Phishing        | 0.98       | Yes      |
| 2 | Phishing     | Phishing        | 0.95       | Yes      |
| 3 | Legitimate   | Legitimate      | 0.92       | Yes      |
| 4 | Phishing     | Phishing        | 0.96       | Yes      |
| 5 | Legitimate   | Legitimate      | 0.94       | Yes      |
| 6 | Legitimate   | Legitimate      | 0.90       | Yes      |
| 7 | Phishing     | Legitimate      | 0.60       | No       |
| 8 | Phishing     | Phishing        | 0.97       | Yes      |
| 9 | Legitimate   | Legitimate      | 0.91       | Yes      |
|10|  Legitimate   |Legitimate|      | 0.89       | Yes      |
```
### Confusion Matrix
|                        | Predicted: Phishing | Predicted: Legitimate |
| ---------------------- | ------------------- | --------------------- |
| **Actual: Phishing**   | TP = 4              | FN = 1                |
| **Actual: Legitimate** | FP = 0              | TN = 5                |

### Calculated Metrics
- **Accuracy:** 90%
- **Precision:** 100%
- **Recall:** 80%
- **F1 Score:** 88.9%
**Interpretation**
The model performed well with high precision, meaning it rarely labeled legitimate emails as phishing. However, recall was slightly lower because one phishing email was misclassified as legitimate. Increasing training data and adding more diverse phishing examples would improve recall and overall performance.
---
## Part B: Generic vs Fine-Tuned Model Comparison
### Models Tested
1. **Generic:** distilbert-base-uncased-finetuned-sst-2-english (sentiment)
2. **Fine-Tuned A:** ealvaradob/bert-finetuned-phishing — Phishing detection
3. **Fine-Tuned B:** openai-community/roberta-base-openai-detector — AI-generated text detection
``` **Results**

| Input    | Generic Label (Score) | Fine-Tuned A Label (Score) | Fine-Tuned B Label (Score) | Best Model   |
| -------- | --------------------- | -------------------------- | -------------------------- | ------------ |
| Record 1 | Negative (0.99)       | Phishing (0.9999)          | Real (0.97)                | Fine-Tuned A |
| Record 2 | Positive (0.88)       | Benign (0.98)              | Real (0.94)                | Fine-Tuned A |
| Record 3 | Negative (0.92)       | Phishing (0.99)            | Real (0.95)                | Fine-Tuned A |
| Record 4 | Positive (0.85)       | Benign (0.97)              | Real (0.93)                | Fine-Tuned A |
| Record 5 | Negative (0.91)       | Phishing (0.99)            | Real (0.96)                | Fine-Tuned A |
```
## Analysis
**Generic model strengths:** The generic sentiment model performed well when phishing messages contained strong negative wording or urgency language.
**Generic model weaknesses:** The generic model struggled to classify phishing accurately because it focuses on sentiment instead of security-related indicators.
**Fine-tuned model advantage:** The phishing-specific model consistently identified phishing emails with high confidence, outperforming the generic sentiment model.
**Biggest surprise:** The AI-generated text detection model was not useful for phishing detection, highlighting the importance of selecting task-specific models.

# Recommended Model for My Capstone Component
**Component:** Threat Classification Engine (Feed Collector)

**Primary model:** [ealvaradob/bert-finetuned-phishing] — Best performance for phishing detection

**Confidence threshold:** 0.85 — Helps reduce false positives while maintaining high detection accuracy

**Priority metric:** Recall — Missing a phishing attack is more dangerous than flagging a legitimate email

## Limitations & Next Steps
The current models rely on pre-trained datasets and may not detect new phishing techniques. With more time and data, I would fine-tune a custom model using real threat intelligence feeds and security datasets. I would also test additional models such as cybersecurity-specific transformers and ensemble approaches. Future improvements include expanding the dataset, improving evaluation metrics, and implementing real-time detection capabilities.
