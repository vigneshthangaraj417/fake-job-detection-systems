# System User Manual

This manual details how to navigate and use the **AI-Based Fake Job Posting Detection System** as a Regular User or System Administrator.

---

## 🔑 Authentication & Entry

1. **Sign Up**: Navigate to the landing page and click **Get Started**. Provide a unique username, valid email, and confirm a secure password to register.
2. **Sign In**: Click **Sign In** from the landing page. Input your username and password. You can toggle password visibility using the eye icon.

---

## 📊 User Dashboard

Upon logging in, you will be redirected to the User Dashboard:
* **Metrics Panel**: Review cards detailing your total scanned jobs count, real postings verified, and fraudulent scams blocked.
* **Recent Activity Feed**: View your last five predictions with color-coded safety badges (Legit/Fake) and exact model confidence percentages.
* **Model Specs Sidebar**: Details the active classifier, training dataset row count, and system accuracy values.

---

## 🔍 Job Prediction (Scanner)

To verify a job listing:
1. Click **Detect Job** in the sidebar.
2. Fill out the form fields. The **Job Title** and **Job Description** fields are mandatory. Provide as much detail as possible (salaries, company name, location, requirements) to increase prediction accuracy.
3. Click **Analyze Job Listing**. A loading animation will trigger.
4. **Read the Verdict**:
   * **Safe / Legit (Green Badge)**: Indicates a low risk of fraud. Review the positive traits listed in the explanation.
   * **High Risk / Fake Job (Red Badge)**: Indicates high probability of a scam. Check the generated bullet points for highlighted **Red Flags** (e.g. wire transfer keywords, communication outside normal channels).

---

## 📂 Search & History Hub

Click **Search Checks** in the sidebar:
* Search previous predictions by entering keywords (matching job titles, company profiles, or locations).
* Filter rows by verdict classification (All, Real, Fake).
* Click on any search result row to expand an **accordion drawer** showing the full context details (salary, description summary) alongside the AI Diagnostic explanation report.

---

## ⚙️ Account Management

Click **Profile** in the sidebar to configure account settings:
* **Account Details Tab**: Update your profile registration email.
* **Security Settings Tab**: Change your password (requires verifying your current password).
* **Danger Zone Tab**: Permanently delete your user account. *Warning: This deletes all your prediction search records and is irreversible.*

---

## 🛡️ Administrative Controls (Admin Center)

*Note: Only visible if signed in with an Administrator account (e.g. username `admin`).*

Click **Admin Center** in the sidebar:

### 1. Account Management Tab
Review all user records in a table format. Admins can permanently delete user accounts (which cascades and deletes their history). Self-deletion is blocked to preserve admin credentials.

### 2. Global Predictions Log
Browse all scans conducted by every registered account.

### 3. Model & Dataset Management
* **Upload Dataset**: Choose a `.csv` training file and click **Upload and Retrain Classifiers**.
* **Asynchronous Progress Logs**: An alert banner will appear at the top of the viewport when training starts. It polls retraining status in the background and reports details (e.g., "Merging rows...", "Comparing models..."). Once complete, the page auto-reloads.
* **Accuracy Comparisons**: The right side displays a leaderboard showing accuracy, precision, and F1 scores of all trained models (Logistic Regression, Naive Bayes, Decision Trees, Random Forests, SVMs).
