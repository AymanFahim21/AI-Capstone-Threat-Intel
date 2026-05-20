# Week 7: RAG Security Knowledge Assistant — Evaluation Report

## 1. Setup Summary

| Component | Configuration |
|---|---|
| **Chatbot Name** | Security Knowledge Assistant |
| **LLM** | `llama-3.3-70b-versatile` through Groq |
| **Temperature** | `0.3` |
| **Embeddings** | HuggingFace Inference Embedding |
| **Vector Store** | In-Memory Vector Store |
| **Retriever Top K** | Default value, likely `4` |
| **Text Splitter** | Recursive Character Text Splitter |
| **Chunk Size** | `1000` |
| **Chunk Overlap** | `200` |
| **Source Documents Returned** | Enabled |

### Documents Loaded

The chatbot was built using three uploaded `.txt` documents:

1. `mitre-lateral-movement.txt`
2. `mitre-initial-access.txt`
3. `mitre-credential-access.txt`

Since the files were text documents, page counts were not shown. Each file appeared to be a short text-based security reference document.

---

## 2. Test Results

| # | Question | Used Documents? | Quality | Notes |
|---|---|---|---|---|
| 1 | What are common techniques for credential access? | Yes | Good | The chatbot used the uploaded documents and mentioned credential access techniques such as Adversary-in-the-Middle and exploitation for credential access. The answer was related to the source documents and mostly accurate. |
| 2 | How does phishing relate to initial access in the ATT&CK framework? | Yes | Good | The chatbot correctly explained that phishing is an Initial Access technique in MITRE ATT&CK. It also explained targeted phishing, spearphishing, and non-targeted phishing. |
| 3 | What is lateral movement and what techniques do attackers use? | Yes | Good | The chatbot correctly described lateral movement as attackers moving through systems after gaining access. It also mentioned remote access tools, legitimate credentials, and exploitation of remote services. |
| 4 | What does the NIST framework recommend for the Detect function? | Yes | Wrong | The chatbot returned “Hmm, I’m not sure.” This shows that the chatbot either did not have enough NIST-related information in the uploaded documents or could not retrieve the correct context. |
| 5 | What is the difference between spearphishing attachment and spearphishing link? | Yes | Wrong | The chatbot again responded “Hmm, I’m not sure.” Even though source document chips appeared, the chatbot did not provide the expected comparison. |

---

## 3. Edge Case Observations

| Edge Case | Observation |
|---|---|
| **Unrelated Question** | When the question was outside the uploaded document context, the chatbot followed the prompt rule and responded with “Hmm, I’m not sure.” This helped prevent hallucination. |
| **Topic Not in Documents** | For the NIST Detect function question, the chatbot could not answer because the uploaded files mainly focused on MITRE ATT&CK topics, not the NIST Cybersecurity Framework. |
| **Similar but Missing Topic** | For the spearphishing attachment vs. spearphishing link question, the chatbot failed to answer clearly. This may mean the Initial Access document did not include enough detail or the retrieved chunks were not specific enough. |

---

## 4. Settings Experiments

| Setting Changed | Observation |
|---|---|
| **Temperature** | The chatbot used a low temperature of `0.3`, which made the answers more focused and less creative. This helped keep responses grounded in the uploaded documents. |
| **Chunk Size** | The chunk size was set to `1000`, which worked well for broad questions like credential access and lateral movement. However, smaller chunks might help with more specific questions such as comparing spearphishing attachment and spearphishing link. |
| **Chunk Overlap** | The chunk overlap was `200`, which helped preserve context between chunks. This is useful when a technique description continues across chunk boundaries. |
| **Top K** | Top K appeared to use the default value, likely `4`. Increasing Top K could improve retrieval for questions where the chatbot responded with “Hmm, I’m not sure,” because it would retrieve more document chunks. |

---

## 5. Reflection

### What surprised you about how RAG works?

What surprised me is that the chatbot does not truly “know” the whole document at once. It depends on retrieving the right chunks from the vector store. If the correct chunk is not retrieved, the chatbot may fail even if the answer exists somewhere in the document.

### How could you improve this chatbot for real-world use?

I would improve the chatbot by adding more complete documents, including NIST Cybersecurity Framework content and more detailed MITRE ATT&CK technique descriptions. I would also increase Top K, improve document chunking, and add a stronger prompt that explains when information is missing instead of only saying “Hmm, I’m not sure.”

### How might you use RAG in your capstone project?

I could use RAG in my threat intelligence dashboard to answer questions from collected security reports, CVEs, MITRE ATT&CK techniques, and IOC data. For example, a user could ask, “What attack techniques are related to this CVE?” or “What recommended actions should we take for this threat?” The chatbot could then answer using stored threat intelligence documents instead of relying only on the model’s general knowledge.

---

## Overall Conclusion

The RAG Security Knowledge Assistant performed well when the questions matched the uploaded MITRE ATT&CK documents. It gave strong answers for credential access, phishing as initial access, and lateral movement. However, it struggled when the question required information that was missing or not retrieved clearly, such as the NIST Detect function and the difference between spearphishing attachment and spearphishing link. Overall, the chatbot showed how useful RAG can be, but also showed that document quality, chunking, and retrieval settings are important for accurate results.
