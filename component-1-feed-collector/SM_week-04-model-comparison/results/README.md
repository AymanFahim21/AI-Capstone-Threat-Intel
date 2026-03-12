# Week 4: Model Comparison

This week we evaluated several AI models to determine which model works best for analyzing cybersecurity text data within our system.

The models were tested on **5 cybersecurity-related text samples** to evaluate their suitability for the **Feed Collector component** of our **AI Capstone Threat Intelligence Dashboard** project.

---

## Models Tested

The following models were integrated into our **n8n workflow pipeline** and evaluated:

- **HF Sentiment (distilbert-base-uncased-finetuned-sst-2-english)**  
  Used for sentiment classification to quickly detect potentially suspicious or negative log activity.

- **HF Zero-Shot (facebook/bart-large-mnli)**  
  Used to classify log entries into security-related categories without additional training.

- **HF NER (bert-large-NER)**  
  Used to extract entities such as IP addresses, usernames, systems, or services mentioned in log data.

- **Groq Llama 3 8B**  
  Used for contextual classification of cybersecurity events using a large language model.

---

## Findings

After comparing the models across **accuracy, confidence score, speed, and integration ease**, we recommend:

**Groq Llama 3 8B** for the **Feed Collector component** because it provides the most accurate contextual understanding of cybersecurity-related events and log data.

The model was particularly effective at identifying **potential threats and suspicious activity** compared to traditional classification models.

---

## Full Analysis

See **`results/SM_report.md`** for the complete analysis, including:

- Model comparison results
- Detailed evaluation of each test record
- Strengths and limitations of each model
- Recommended model architecture for the project
