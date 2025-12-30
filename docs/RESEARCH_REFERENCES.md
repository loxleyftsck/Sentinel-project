# 📚 Research & References

**Project**: SENTINEL - AI-Powered Insider Trading Compliance Monitoring
**Researcher**: Herald Michain Samuel Theo Ginting
**Core Methodology**: Retrieval-Augmented Generation (RAG) + Domain-Specific Risk Scoring

---

## 🔬 ACADEMIC REFERENCES

### 1. Large Language Models & RAG

- **Lewis, P., et al. (2020)**. *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks."* Advances in Neural Information Processing Systems (NeurIPS). [Fundamental paper for the RAG architecture used in SENTINEL].
- **Thoppilan, R., et al. (2022)**. *"LaMDA: Language Models for Dialog Applications."* arXiv preprint arXiv:2201.08239. [Context for LLM reasoning capabilities].

### 2. Machine Learning in Financial Surveillance

- **Bhattacharyya, S., et al. (2011)**. *"Data mining for credit card fraud detection: A comparative study."* Decision Support Systems. [Foundational concepts for anomaly detection applied to financial markets].
- **Goldstein, I., & Yang, L. (2015)**. *"Information Design in Financial Markets."* Annual Review of Financial Economics. [Research on information asymmetry, relevant to insider trading mechanics].

### 3. Insider Trading Detection

- **Huddart, S., & Ke, B. (2007)**. *"Information Content of Stock Purchases by Insiders and Brokers."* Journal of Accounting and Economics. [Statistical patterns of insider behavior].
- **Donalson, D. (2018)**. *"Machine Learning Applications for Insider Trading Detection."* Financial Intelligence Review.

---

## ⚖️ REGULATORY FRAMEWORKS

### 1. Indonesia Financial Services Authority (OJK)

- **POJK No. 31/POJK.04/2015**: *"Disclosure of Information or Material Facts by Issuers or Public Companies."* [The primary logic used in SENTINEL's compliance check].
- **POJK No. 78/POJK.04/2017**: *"Transactions of Securities Not Subject to Insider Trading."* [Used for defining 'Safe Harbor' rules in the analysis engine].

### 2. Indonesia Stock Exchange (IDX)

- **IDX Rule No. I-E**: *"Reporting Obligations."* [Source for reporting timelines and disclosure standards].

---

## 🛠️ TECHNOLOGICAL FOUNDATIONS

### 1. LangChain Framework

- Chase, H. (2023). *"LangChain: Building Applications with LLMs Through Composability."* [Library used for orchestrating the RAG pipeline].

### 2. Vector Databases (ChromaDB)

- Chroma Team. (2023). *"Chroma: The AI-native Open-Source Embedding Database."* [Infrastructure for high-dimensional regulatory data retrieval].

### 3. Local LLM Inference (Ollama)

- Ollama Project. (2024). *"Ollama: Get up and running with large language models locally."* [Used for private, secure, and on-premise AI inference].

---

## 🧮 MATHEMATICAL METHODOLOGY

### 1. Risk Scoring Formula

SENTINEL uses a non-linear weighted sum model for risk calculation:

$$Risk\_Score = \sum_{i=1}^{n} (w_i \cdot s_i) \cdot \prod_{j=1}^{m} k_j$$

Where:

- $w_i$: Component weight (Regulatory, Statistical, Behavioral)
- $s_i$: Raw component score [0-100]
- $k_j$: Critical multipliers (e.g., proximity to material news)

### 2. Hybrid Anomaly Detection

The system combines:

- **Z-Score analysis** for volume spikes
- **Semantic Similarity** for regulation alignment
- **Temporal Correlation** with disclosure event windows

---

## 🧑‍🔬 RESEARCHER CONTACT

**Herald Michain Samuel Theo Ginting**

- **Role**: AI Engineer / Quantitative Researcher
- **Specialization**: Financial Compliance & Intelligent Systems
- **GitHub**: [loxleyftsck](https://github.com/loxleyftsck)
- **Project Goal**: To bridge the gap between complex financial regulations and automated AI-driven compliance monitoring.

---

> [!NOTE]
> This document serves as the theoretical and regulatory foundation for the SENTINEL project.
