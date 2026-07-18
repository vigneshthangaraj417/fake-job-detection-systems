# Installation and Setup Guide

This guide details the step-by-step instructions required to run the **AI-Based Fake Job Posting Detection System** on your local machine for development and testing.

---

## 💻 System Prerequisites

Before proceeding, ensure your system meets the following specifications:
* **Operating System**: Windows 10/11, macOS Catalina or higher, Ubuntu 20.04 LTS or higher.
* **Python**: Version `3.8`, `3.9`, or `3.10` installed. (Python 3.11/3.12 are supported, but scikit-learn binary wheels compile faster on 3.8-3.10).
* **RAM**: Minimum 4GB (8GB recommended to speed up SVM model training).
* **Storage**: 100MB free space.

---

## 🛠️ Installation Steps

Follow these terminal commands sequentially to deploy:

### Step 1: Clone the Codebase
Extract the project ZIP folder or clone from git:
```bash
git clone https://github.com/username/fake-job-detection.git
cd "AI-Based Fake Job Posting Detection System"
```

### Step 2: Establish a Virtual Environment
Isolating dependencies ensures no conflicts arise with standard system packages:
```bash
# Windows (Command Prompt or PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux (Terminal)
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Dependencies
Install the required packages using the requirements configuration:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Populate Data & Pretrain Models
Execute the scripts to compile the local database, seed mock Kaggle dataset, and train Scikit-learn classifiers:
```bash
# 1. Generate local job postings csv file (400 records)
python dataset/generate_mock_data.py

# 2. Train classifiers & save vectorizer + best model
python model/pipeline.py
```
After execution, verify that:
* A CSV file is created in `dataset/fake_job_postings.csv`.
* Model files `best_model.pkl`, `vectorizer.pkl`, and `training_report.json` exist under the `trained_model/` folder.

### Step 5: Start the Flask Dev Server
Start the web application:
```bash
python app.py
```
The server will boot up in debug mode:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```
Open a browser and type `http://127.0.0.1:5000` to access the home portal.

---

## 🔐 Default Admin & User Accounts

The database SQLite seeds default credentials upon creation. You may sign in instantly:

| Account Type | Username | Password |
| :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` |
| **Regular User** | `user` | `password123` |

---

## ⚠️ Troubleshooting FAQ

### Q1: `ModuleNotFoundError: No module named 'joblib'` (or pandas/sklearn)
* **Fix**: Ensure your virtual environment is active (you should see `(venv)` prefix in your terminal prompt) before running `pip install -r requirements.txt`.

### Q2: Training pipeline crashes on SVM (`Support Vector Machine`) training
* **Fix**: SVM classifiers can take long on extremely large text collections. If it hangs on low-spec PCs during retraining, you can modify `model/pipeline.py` to disable SVM or lower the max features value.

### Q3: `Port 5000 is already in use`
* **Fix**: Another application (like AirPlay on macOS) might be occupying port 5000. You can start the server on a different port:
  ```python
  # In app.py line 685:
  app.run(debug=True, port=8080)
  ```
