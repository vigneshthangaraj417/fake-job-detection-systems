import os
import json
import re
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', ' ', text)
    # Keep only letters and spaces
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_and_evaluate(csv_path='dataset/fake_job_postings.csv'):
    print("Starting ML Pipeline training and comparison...")
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file not found at {csv_path}. Please generate or upload it first.")
        
    # 1. Load Data
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset with {len(df)} rows.")
    
    # Fill NAs in text columns
    text_cols = [
        'title', 'location', 'department', 'company_profile', 'description', 
        'requirements', 'benefits', 'employment_type', 'required_experience', 
        'required_education', 'industry', 'function'
    ]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna("")
        else:
            df[col] = ""
            
    # Combine text features
    df['combined_text'] = (
        df['title'] + " " +
        df['location'] + " " +
        df['department'] + " " +
        df['company_profile'] + " " +
        df['description'] + " " +
        df['requirements'] + " " +
        df['benefits'] + " " +
        df['employment_type'] + " " +
        df['required_experience'] + " " +
        df['required_education'] + " " +
        df['industry'] + " " +
        df['function']
    )
    
    # Clean combining text
    print("Preprocessing and cleaning text features...")
    df['cleaned_text'] = df['combined_text'].apply(clean_text)
    
    # Target
    y = df['fraudulent'].fillna(0).astype(int).values
    X = df['cleaned_text'].values
    
    # 2. Vectorization
    print("Vectorizing text using TF-IDF...")
    # Using built-in sklearn English stop words
    vectorizer = TfidfVectorizer(stop_words=list(ENGLISH_STOP_WORDS), max_features=5000, ngram_range=(1, 2))
    X_vectorized = vectorizer.fit_transform(X)
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_vectorized, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Train set shape: {X_train.shape}, Test set shape: {X_test.shape}")
    
    # 4. Model Training & Comparison
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Naive Bayes': MultinomialNB(),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Support Vector Machine': SVC(probability=True, random_state=42)
    }
    
    results = {}
    best_accuracy = -1
    best_model_name = ""
    best_model_obj = None
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        # Predict
        y_pred = model.predict(X_test)
        
        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        
        results[name] = {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1_score': float(f1),
            'confusion_matrix': {
                'tn': int(tn),
                'fp': int(fp),
                'fn': int(fn),
                'tp': int(tp)
            }
        }
        
        print(f"{name} - Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
        
        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model_obj = model
            
    print(f"\nBest Model selected: {best_model_name} with Accuracy: {best_accuracy:.4f}")
    
    # 5. Save best model and vectorizer
    os.makedirs('trained_model', exist_ok=True)
    model_path = os.path.join('trained_model', 'best_model.pkl')
    vec_path = os.path.join('trained_model', 'vectorizer.pkl')
    report_path = os.path.join('trained_model', 'training_report.json')
    
    joblib.dump(best_model_obj, model_path)
    joblib.dump(vectorizer, vec_path)
    
    # Save training report
    report = {
        'best_model': best_model_name,
        'dataset_size': len(df),
        'train_size': X_train.shape[0],
        'test_size': X_test.shape[0],
        'metrics': results
    }
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"Model saved to {model_path}")
    print(f"Vectorizer saved to {vec_path}")
    print(f"Training report saved to {report_path}")
    
    return report

if __name__ == '__main__':
    train_and_evaluate()
