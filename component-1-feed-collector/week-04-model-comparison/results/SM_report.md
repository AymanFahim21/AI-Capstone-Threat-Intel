# Model Comparison Report — Week 4
Name: Sangram Mathews
Date: March 11, 2026
Capstone Project: Threat Intelligence Feed Dashboard
My Component: Feed Collector / AI Log Analyzer

## Test Setup
Input dataset:
5 cybersecurity-related text samples collected from threat intelligence feeds and log records. The dataset included:
•	2 high-severity alerts (malware activity / suspicious login attempts)
•	1 ambiguous case (unusual but not confirmed malicious behavior)
•	2 benign records (normal operational activity)
These records were stored in Airtable and processed through the n8n workflow pipeline.

Models Tested
The workflow evaluated the following models through HuggingFace and Groq APIs:
1.	distilbert-base-uncased-finetuned-sst-2-english
o	Sentiment classification
o	Used to quickly detect potentially negative or suspicious log activity
2.	facebook/bart-large-mnli (Zero-Shot Classification)
o	Used to classify log entries into security-related categories without additional training
3.	facebook/bart-large-mnli (NER extraction)
o	Used to identify entities such as IP addresses, systems, organizations, or services mentioned in logs
4.	Groq Llama 3 8B
o	Large language model used for contextual classification of cybersecurity events

**Evaluation criteria:** label accuracy, confidence score, speed, ease of
integration in n8n
## Results Summary

| Record | Sentiment | Zero-Shot Classification | NER Entities | Groq Classification |
|-------|-----------|--------------------------|--------------|--------------------|
| 1 | Negative (0.92) | Malware Activity | IP address detected | High risk threat |
| 2 | Negative (0.88) | Unauthorized Login Attempt | Username, Server | Suspicious activity |
| 3 | Neutral (0.61) | Network anomaly | Internal host | Possible anomaly |
| 4 | Positive (0.79) | Routine system update | Software version | Benign activity |
| 5 | Neutral (0.68) | Normal traffic | None | Normal system log |

## Analysis
Where models agreed
The models generally agreed on the clearly malicious and clearly benign records.
For example:
•	Record 1 and Record 2
o	Sentiment detected strong negative signals
o	Zero-Shot classified them as security incidents
o	Groq confirmed threat classifications
This indicates that multiple models can reliably detect high-risk cybersecurity events.
________________________________________
Where models disagreed
The models differed mainly on ambiguous events.
Example:
Record 3
•	Sentiment: Neutral
•	Zero-Shot: Network anomaly
•	Groq: Possible anomaly
This difference likely occurs because:
•	Sentiment models analyze language tone
•	Zero-Shot models analyze semantic classification
•	LLM models use contextual reasoning
This highlights why combining multiple models improves detection accuracy.

Most Accurate Model Overall:
The Groq Llama 3 8B model produced the most meaningful classifications.
Reasons:
•	Better understanding of security context
•	More detailed classification reasoning
•	More flexible handling of ambiguous log entries
________________________________________
Fastest / Most Practical Model:
The DistilBERT Sentiment model was the fastest.
Advantages:
•	Very low latency
•	Easy to integrate
•	Works well for initial filtering
However, it lacks deeper contextual understanding.

Recommended Models for My Capstone Component
Component: Feed Collector (Threat Intelligence Processing)

Primary Model
Groq Llama 3 8B
Reason:
Provides context-aware classification of security events, which is essential when analyzing real-world cybersecurity logs and threat intelligence feeds.
________________________________________
Secondary Model
facebook/bart-large-mnli (Zero-Shot)
Reason:
Useful for categorizing threat types without additional training.
________________________________________
Rejected Models and Why
DistilBERT Sentiment
Not ideal for final threat classification because:
•	Sentiment analysis does not always correlate with security risk level
•	Cannot detect specific cybersecurity patterns
________________________________________
NER Model
While helpful for extracting entities such as IP addresses and systems, it does not provide threat classification, so it works better as a supporting feature rather than the main detection model.


Failure Cases and Limitations:
One example occurred when analyzing Record 3, which contained unusual network behavior but no explicit attack indicators.
•	Sentiment model returned neutral
•	Zero-Shot labeled it network anomaly
•	Groq labeled it possible anomaly
This shows that AI models may struggle with uncertain or incomplete log data.
In production environments, this limitation suggests that AI predictions should be combined with rule-based detection systems and analyst review.
________________________________________
Next Steps:
If more time were available, the following improvements would be tested:
•	Expanding the dataset to 50–100 log samples
•	Testing additional models such as:
o	bert-base-cybersecurity models
o	OpenAI GPT-4 style classification models
•	Evaluating model accuracy against labeled cybersecurity datasets
•	Implementing a confidence threshold system for automated alerts
This would help improve the reliability and scalability of the AI-driven threat intelligence pipeline.

