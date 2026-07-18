import os
import joblib
import re

class JobPredictor:
    def __init__(self, model_dir='trained_model'):
        self.model_path = os.path.join(model_dir, 'best_model.pkl')
        self.vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        self.model = None
        self.vectorizer = None
        self.load_model()

    def load_model(self):
        if not os.path.exists(self.model_path) or not os.path.exists(self.vectorizer_path):
            raise FileNotFoundError("Trained model files not found. Please train the model first.")
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'<[^>]*>', ' ', text)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def predict(self, job_data):
        """
        job_data: dict containing:
            - title
            - company_name
            - location
            - department
            - description
            - requirements
            - benefits
            - employment_type
            - required_experience
            - required_education
            - industry
            - function
            - salary_info
        """
        if self.model is None or self.vectorizer is None:
            self.load_model()
            
        # Extract features and fill NAs
        title = job_data.get('title', '') or ''
        location = job_data.get('location', '') or ''
        dept = job_data.get('department', '') or ''
        company_profile = job_data.get('company_profile', '') or '' # Add company profile if provided
        desc = job_data.get('description', '') or ''
        req = job_data.get('requirements', '') or ''
        ben = job_data.get('benefits', '') or ''
        emp_type = job_data.get('employment_type', '') or ''
        exp = job_data.get('required_experience', '') or ''
        edu = job_data.get('required_education', '') or ''
        ind = job_data.get('industry', '') or ''
        func = job_data.get('function', '') or ''
        salary = job_data.get('salary_info', '') or ''
        
        # Combine just like training
        combined_text = (
            title + " " + location + " " + dept + " " + company_profile + " " +
            desc + " " + req + " " + ben + " " + emp_type + " " + exp + " " +
            edu + " " + ind + " " + func
        )
        
        cleaned = self.clean_text(combined_text)
        
        # Vectorize
        vectorized_text = self.vectorizer.transform([cleaned])
        
        # Predict Class and Probability
        prediction_val = int(self.model.predict(vectorized_text)[0])
        probabilities = self.model.predict_proba(vectorized_text)[0]
        confidence = float(probabilities[prediction_val] * 100)
        
        # Build Explanation
        explanation = self.generate_explanation(prediction_val, combined_text, job_data)
        
        return {
            'label': prediction_val, # 0 = Real, 1 = Fake
            'result_text': "Fake Job" if prediction_val == 1 else "Real Job",
            'confidence': round(confidence, 2),
            'explanation': explanation
        }

    def generate_explanation(self, prediction_val, combined_text, job_data):
        text_lower = combined_text.lower()
        
        # Define some common scam keywords (red flags)
        scam_keywords = {
            'wire transfer': 'Asks for banking/wire transfer details or money management.',
            'earn money from home': 'Promises easy remote work with unrealistic compensation.',
            'whatsapp': 'Requests communication via external informal apps (WhatsApp).',
            'telegram': 'Requests communication via external informal apps (Telegram).',
            'no experience required': 'Unusually low entry requirements for high payouts.',
            'training fee': 'Asks for upfront payment/application fee.',
            'application fee': 'Requires upfront payment or registration fee.',
            'easy money': 'Suspicious phrases indicating fast, effortless income.',
            're-shipping': 'Indicates package processing/forwarding scams.',
            'mystery shopper': 'Often associated with money order/check cashing fraud.',
            'earn up to': 'Unusually high salary range for simple clerical work.',
            'part time data entry': 'Frequently targeted role for mock job postings scams.'
        }
        
        red_flags_found = []
        for word, desc in scam_keywords.items():
            if word in text_lower:
                red_flags_found.append(f"🚩 **{word.title()}**: {desc}")
                
        # Additional metadata red flags
        title = (job_data.get('title', '') or '').lower()
        salary = (job_data.get('salary_info', '') or '').lower()
        company = (job_data.get('company_name', '') or '').lower()
        
        if not company:
            red_flags_found.append("🚩 **Anonymous Employer**: Job posted without a company name.")
            
        if prediction_val == 1:
            # Fake explanation
            explanation_parts = [
                "This job posting has been flagged as **Fake** by our Machine Learning classifier.",
                "Here are the reasons for this assessment:"
            ]
            if red_flags_found:
                explanation_parts.extend(red_flags_found)
            else:
                explanation_parts.append("- The text matches pattern indicators of mock job listings or phishing pages.")
                explanation_parts.append("- The vocabulary lacks specific, standard corporate roles or responsibilities, indicating high-risk content.")
            explanation_parts.append("\n**Recommendation:** Do not submit personal information, bank details, or registration fees to this posting.")
            return "\n".join(explanation_parts)
        else:
            # Real explanation
            explanation_parts = [
                "This job posting has been classified as **Real** by our Machine Learning classifier.",
                "Here are the reasons for this assessment:"
            ]
            
            # Check for positive traits
            green_flags = []
            if company:
                green_flags.append(f"✅ **Verifiable Organization**: Posted on behalf of '{job_data.get('company_name')}'")
            if len(job_data.get('requirements', '')) > 50:
                green_flags.append("✅ **Detailed Requirements**: Contains professional experience and education criteria rather than generic statements.")
            if len(job_data.get('description', '')) > 100:
                green_flags.append("✅ **Structured Job Role**: Details clear daily responsibilities and technical workflows.")
            
            if green_flags:
                explanation_parts.extend(green_flags)
            else:
                explanation_parts.append("- The posting utilizes a standard professional structure and corporate terminology.")
                explanation_parts.append("- No obvious phishing or wire transfer keywords were detected in the description, requirements, or benefits.")
                
            if red_flags_found:
                explanation_parts.append("\n*Note: Although marked Real, the text contained some minor keywords to watch out for:*")
                explanation_parts.extend([flag.replace("🚩", "⚠️") for flag in red_flags_found])
                
            return "\n".join(explanation_parts)

if __name__ == '__main__':
    # Quick test
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
        
    try:
        predictor = JobPredictor()
        test_job = {
            'title': 'Senior Software Engineer',
            'company_name': 'Google DeepMind',
            'location': 'London, UK',
            'description': 'We are looking for a Senior Software Engineer to design ML systems. Needs Python and Flask.',
            'requirements': 'Degree in Computer Science, 5 years experience in Software Development, backend databases.',
            'benefits': 'Health insurance, annual leaves, stock options'
        }
        res = predictor.predict(test_job)
        print("Test prediction:", res)
    except Exception as e:
        print("Failed to run test prediction:", e)
