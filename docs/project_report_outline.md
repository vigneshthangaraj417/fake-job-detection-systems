# Project Report Outline

This document outlines the standard academic structure for the final-year college project report: **AI-Based Fake Job Posting Detection System using Machine Learning**.

---

## 📘 Title Page & Certificates
* **Project Title**: AI-Based Fake Job Posting Detection System using Machine Learning
* **Candidate Declarations & Certificates**
* **Acknowledgements**
* **Abstract**: Short overview of the employment fraud crisis, NLP techniques, and system results.

---

## 📂 Chapter Outline

### Chapter 1: Introduction
* **1.1 Background & Motivation**: The rise of remote work and corresponding recruitment scams (identity theft, wire transfer mules, check fraud).
* **1.2 Problem Statement**: Challenges in identifying fake job advertisements manually from large job portals.
* **1.3 Project Objectives**: Developing an automated detection framework, visualizing historical trends, and providing admin model retraining capabilities.
* **1.4 Project Scope**: Desktop and mobile web deployment targeting job seekers and portal admins.

### Chapter 2: Literature Review
* **2.1 Review of Existing Systems**: Traditional heuristic rule checks, limitations, and manual flags.
* **2.2 Machine Learning Classifiers in Text Categorization**:
  * Logistic Regression (Linear models efficiency).
  * Multinomial Naive Bayes (Bag-of-words probability).
  * Decision Trees and Random Forests (Non-linear ensembles).
  * Support Vector Machine (Vector space margins).
* **2.3 NLP Feature Extractors**: Term Frequency-Inverse Document Frequency (TF-IDF) vs word embeddings (Word2Vec, GloVe).

### Chapter 3: System Requirements & Specifications
* **3.1 Hardware Requirements**: RAM, Storage, CPU specs.
* **3.2 Software Requirements**: OS, Python dependencies, SQLite, Flask, Chart.js.
* **3.3 Functional Requirements**: Authentications, Scan portal, Admin datasets uploads, Analytics rendering.
* **3.4 Non-Functional Requirements**: Security, responsiveness, explanation clarity, thread safety.

### Chapter 4: System Design & Architecture
* **4.1 Overall Block Diagram**:
  ```
  [User Inputs Form] ──> [Flask API] ──> [NLP Cleaner] ──> [TF-IDF Vectorizer] ──> [ML Classifier] ──> [Verdict HTML]
  ```
* **4.2 Database Schema Design**:
  * `users` Table.
  * `predictions` Table (cascading on user deletion).
  * `uploaded_datasets` Table.
* **4.3 Flow Charts**:
  * User authentication flow.
  * Asynchronous background retraining loop flow.

### Chapter 5: System Implementation
* **5.1 Text Preprocessing**: Lowercasing, HTML tags stripping, special character filtering, extra whitespace trimming.
* **5.2 Feature Extraction**: Bag-of-words tokenization and TF-IDF vectorization with English stop words.
* **5.3 Model Training Pipeline**: Data split details (80-20 train-test ratio), training loop parameters, and saving model files using Joblib.
* **5.4 UI Styling Design**: Implementation of custom CSS Glassmorphism variables, dark mode triggers, and Chart.js endpoints integration.

### Chapter 6: Results, Testing & Evaluation
* **6.1 Performance Evaluation Metrics**:
  * Accuracy ($(\text{TP}+\text{TN}) / \text{Total}$).
  * Precision ($\text{TP} / (\text{TP}+\text{FP})$).
  * Recall ($\text{TP} / (\text{TP}+\text{FN})$).
  * F1 Score ($2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$).
* **6.2 Confusion Matrix Analysis**: Explaining False Positives (Real jobs marked Fake) vs False Negatives (Scams marked Real).
* **6.3 Model Benchmark Comparison**: Accuracies comparison charts (benchmarking Logistic Regression vs RF vs Naive Bayes vs Decision Trees vs SVM).

### Chapter 7: Conclusion & Future Scope
* **7.1 Summary of Contributions**: Fully modular end-to-end working web application.
* **7.2 Limitations of the Current System**: Static dictionary for keyword checks, dependence on structured CSV schema.
* **7.3 Future Enhancements**: Embedding deep learning models, WHOIS domain lookups, and browser extension integration.

---

## 📚 References & Bibliography
* APA citation format listing Scikit-learn references, Flask tutorials, Kaggle dataset references, and relevant NLP research papers.
