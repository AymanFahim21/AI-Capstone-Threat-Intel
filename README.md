## 👤 Author
- **Sangram Mathews**
- **Ayman Fahim**
- **Darius Taule**
# John Jay College of Criminal Justice

# 🛡️ AI-Capstone-Threat-Intel

A threat intelligence automation and visualization project that collects cybersecurity threat data from multiple sources, stores it in Airtable, enriches it with IOCs, CVEs, summaries, and relevance scores, then displays the results in a Streamlit dashboard for security triage and analysis.

## 📌 Project Overview

This dashboard acts as a lightweight **Security Operations Center-style threat intelligence console**. It is designed to help security analysts quickly review and prioritize threat intelligence from public cybersecurity feeds. Instead of manually checking different sources, this project uses automated n8n workflows to collect, normalize, enrich, and score threat data before sending it into Airtable. The Streamlit dashboard then provides a clean interface for viewing recent threats, CVEs, indicators of compromise, severity levels, and recommended actions. Its goal is not just to display raw data, but to transform raw threat information into **actionable intelligence**.

## 🎯 Purpose

The main purpose of this dashboard is to support **threat intelligence triage**. It helps analysts quickly answer important questions such as:

- Which threats are critical or high priority?
- What indicators of compromise are connected to each threat?
- Which attack types are appearing most often?
- What software or systems are affected?
- Where are suspicious IP indicators located?
- Which threats should be investigated first?

By organizing this information into a visual dashboard, the project helps reduce manual analysis time and supports faster cybersecurity decision-making.

This makes the dashboard useful for:

- Cybersecurity research
- Threat intelligence analysis
- Vulnerability monitoring
- IOC investigation
- Incident response preparation
- Security operations prioritization

## 🔗 Data Sources

The dashboard uses threat intelligence collected from multiple public sources, including:

- **AlienVault OTX**
- **Krebs on Security**
- **NVD CVE**

## ⚙️ Workflow Overview

The project follows a threat intelligence pipeline:

1. Public threat intelligence data is collected from external sources.
2. n8n workflows process the data and extract useful security information.
3. Indicators of compromise are identified, including IPs, domains, URLs, hashes, and emails.
4. Threats are scored based on severity, relevance, and priority.
5. Cleaned and structured records are stored in Airtable.
6. The Streamlit dashboard reads the Airtable data and displays it through tables, charts, maps, and analyst views.

## 🛠️ Technologies Used

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Airtable](https://img.shields.io/badge/Airtable-18BFFF?style=for-the-badge&logo=airtable&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)

## 📊 Dashboard Highlights

- **Executive Summary**
  - Displays total threats, critical threats, high severity threats, unique CVEs, total IOCs, and average relevance score.

- **Analyst Priority Queue**
  - Ranks threats by priority score, severity, and relevance so analysts can focus on the most urgent risks first.

- **Threat Analytics**
  - Visualizes severity distribution, top attack types, severity by source, and affected software.

- **Threat Origin Map**
  - Maps IP-based indicators to show the geographic origin of suspicious infrastructure.

- **Indicators of Compromise**
  - Extracts and displays IP addresses, domains, URLs, and file hashes.

- **Threat Table**
  - Provides a complete searchable and filterable table of actionable threats.

- **Deep Dive View**
  - Allows analysts to select a specific threat and review its severity, source, attack type, affected software, summary, recommended actions, and related IOCs.

- **Alert Preview**
  - Previews critical and high-priority threats that could be sent through Slack or email notifications.

- **Export Options**
  - Supports exporting filtered threat data as CSV, JSON, IOC context CSV, and STIX-like indicator JSON.

## 🎥 Project Demo

<a href="https://www.youtube.com/watch?v=BZNQ5l92Ghs">
  <img width="800" alt="AI Threat Intelligence Dashboard Demo Thumbnail" src="https://github.com/user-attachments/assets/03688281-657b-43c5-9008-4ef2bee187f9" />
</a>




