# AI-Based Fake Job Posting Detection System using Machine Learning

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue.svg)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/library-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end, production-ready web application that leverages advanced Natural Language Processing (NLP) and supervised machine learning algorithms to verify and detect fraudulent job postings. Built with a premium, responsive Glassmorphism frontend and a secure Flask backend.

---

## 🌟 Key Features

* **Instant Fake Job Detection**: Cross-references job descriptions, titles, salaries, locations, and company profiles in real-time.
* **Explainable AI (XAI)**: Provides clear red-flag breakdowns (e.g., upfront payment triggers, telegram apps links, bank transfer requests) instead of just an arbitrary prediction score.
* **Asynchronous Model Retraining**: Admins can upload new CSV datasets and retrain five machine learning models in the background. The system automatically benchmarks accuracy and deploys the highest-performing classifier.
* **Glassmorphic SaaS Analytics**: Premium statistics charts powered by Chart.js showcasing verdicts trends, scanner volume, and active user stats.
* **Secure Session Handling**: Implement password hashing (using Werkzeug security), SQL injection mitigation, and user credential safeguards with SQLite.
* **Dual Dashboard Interface**: Specialized dashboards tailored for active Job Hunters and System Administrators.

---

## 🛠️ Technology Stack

* **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism styling variables), JavaScript (ES6+), Bootstrap 5
* **Backend**: Python 3, Flask framework
* **Machine Learning**: Scikit-Learn, Pandas, NumPy, Joblib
* **Database**: SQLite3
* **Visualization**: Chart.js (Responsive Canvas API integration)

---

## 🤖 Machine Learning Pipeline & Comparisons

The machine learning core uses a standardized NLP pipeline:

```
Data Cleaning  ──>  Text Preprocessing  ──>  TF-IDF Vectorization  ──>  Models Comparison  ──>  Best Model Export
```

We train and benchmark **five** classification algorithms simultaneously during retraining:
1. **Logistic Regression** (Linear Classifier)
2. **Multinomial Naive Bayes** (Probabilistic Classifier)
3. **Random Forest Classifier** (Ensemble Tree-based)
4. **Decision Tree Classifier** (Single Decision path)
5. **Support Vector Machine (SVM)** (Margin Maximization)

*Note: The model with the highest validation accuracy is automatically saved and lazily reloaded on demand for incoming prediction queries.*

---

## 📁 Folder Structure

```
AI-Based Fake Job Posting Detection System/
│
├── app.py                     # Main Flask Application
├── requirements.txt           # Python Project Dependencies
├── README.md                  # Project Documentation Hub
│
├── dataset/
│   ├── fake_job_postings.csv  # Combined CSV dataset
│   └── generate_mock_data.py  # Mock dataset generator script
│
├── model/
│   ├── pipeline.py            # Training & evaluation pipeline
│   └── predictor.py           # Feature merging and prediction engine
│
├── trained_model/
│   ├── best_model.pkl         # Saved Scikit-Learn model
│   ├── vectorizer.pkl         # Saved TF-IDF Vectorizer
│   └── training_report.json   # Model performance metadata metrics
│
├── static/
│   ├── css/
│   │   └── styles.css         # Premium Glassmorphic Layout Styles
│   └── js/
│       └── main.js            # Light/Dark Theme & Progress Polling Script
│
├── templates/                 # Jinja2 Layout Templates
│   ├── base.html              # Main HTML Wrapper
│   ├── index.html             # Home Landing Page
│   ├── login.html             # Secure Sign In Form
│   ├── register.html          # Secure Registration Form
│   ├── dashboard.html         # User Statistics
│   ├── predict.html           # Core Job Scanner Inputs
│   ├── analytics.html         # Interactive Chart.js Graphs
│   ├── search.html            # Query History Explorer
│   ├── profile.html           # Account & Password Management
│   └── admin.html             # Admin controls, uploads, and training
│
├── database/                  # Auto-generated SQLite Database File
│   └── database.db
│
├── uploads/                   # Temporary directory for uploaded CSV files
│
└── docs/                      # Academic Project Reports & Manuals
    ├── installation_guide.md
    ├── user_manual.md
    └── project_report_outline.md
```

---

## 🚀 Quick Start Setup

### Prerequisites
* Python 3.8 or above installed on your local system.

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/fake-job-detection.git
cd fake-job-detection
```

### 2. Set up virtual environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install required packages
```bash
pip install -r requirements.txt
```

### 4. Seed Mock Dataset & Train Model
To seed the initial dataset and run the initial training, execute:
```bash
python dataset/generate_mock_data.py
python model/pipeline.py
```

### 5. Launch the application
```bash
python app.py
```
Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## 🔐 Credentials Seeding (Default Accounts)

On first run, the SQLite database auto-seeds two standard accounts for verification:

* **Administrator Account**:
  * Username: `admin`
  * Password: `admin123`
* **Regular User Account**:
  * Username: `user`
  * Password: `password123`

---

## 🔮 Future Enhancements

* **Deep Learning NLP Model**: Integrate Bi-LSTM or BERT transformer model architectures to increase semantic context understanding.
* **Resume Quality Assessment**: Help users scan their CVs to check if they match job postings keywords.
* **Active Web Scraping Engine**: Pull active job postings straight from public job boards (LinkedIn, Indeed) using BeautifulSoup.
* **Company Domain Check**: Automatically lookup WHOIS registry records of job post email domains to flag newly registered suspicious sites.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
