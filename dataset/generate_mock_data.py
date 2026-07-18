import csv
import os
import random

def generate_dataset():
    os.makedirs('dataset', exist_ok=True)
    filepath = os.path.join('dataset', 'fake_job_postings.csv')
    
    # Kaggle columns
    columns = [
        'job_id', 'title', 'location', 'department', 'salary_range',
        'company_profile', 'description', 'requirements', 'benefits',
        'telecommuting', 'has_company_logo', 'has_questions', 'employment_type',
        'required_experience', 'required_education', 'industry', 'function', 'fraudulent'
    ]
    
    # Vocabularies for mock data
    real_titles = [
        "Software Engineer", "Frontend Developer", "Data Scientist", "Python Developer",
        "Product Manager", "DevOps Engineer", "Digital Marketing Specialist", "Sales Executive",
        "HR Coordinator", "Database Administrator", "Financial Analyst", "UX/UI Designer",
        "Business Analyst", "Customer Support Representative", "Quality Assurance Engineer"
    ]
    
    fake_titles = [
        "Work From Home Data Entry Clerk", "Virtual Assistant - Easy Money",
        "Online Typist - Part Time", "Payment Processing Agent", "Customer Service Agent - Earn Fast",
        "Administrative Assistant (Remote)", "Mystery Shopper / Product Tester", 
        "Financial Agent - Wire Transfer", "Package Processing Assistant", "Urgent Office Help"
    ]
    
    locations = [
        "US, NY, New York", "US, CA, San Francisco", "US, TX, Austin", "GB, LND, London",
        "CA, ON, Toronto", "DE, BY, Munich", "AU, NSW, Sydney", "IN, KA, Bangalore",
        "SG, SG, Singapore", "US, FL, Miami", "US, WA, Seattle", "FR, IDF, Paris"
    ]
    
    departments = ["Engineering", "Product", "Marketing", "Sales", "HR", "Finance", "Operations", "Customer Service", ""]
    
    real_profiles = [
        "We are a leading global software provider helping enterprises accelerate their digital transformation. Founded in 2012, we build scalable software products.",
        "A fast-growing fintech company revolutionizing mobile payments. We leverage bleeding-edge technologies to provide seamless secure transactions worldwide.",
        "An award-winning digital marketing agency. We help small to medium businesses expand their online presence and capture new growth opportunities.",
        "We are an innovative healthcare technology startup. Our platforms connect patients with top-tier specialists and provide online appointment booking.",
        "A major e-commerce retailer offering high-quality fashion and home accessories. We are expanding our operations internationally."
    ]
    
    fake_profiles = [
        "A global conglomerate with diversified interests. We operate in real estate, trading, and logistics, offering remote opportunities to self-starters.",
        "We are an international investment group establishing our footprint in this region. We hire remote workers to optimize operations.",
        "An outsourcing service provider connecting global corporations with flexible remote labor. Start working today and build your financial freedom.",
        ""
    ]
    
    real_descriptions = [
        "We are looking for a Software Engineer to join our core backend team. You will design, build, and maintain efficient, reusable, and reliable code. Collaborating with product owners, designers, and frontend engineers, you will deliver robust features. You will participate in code reviews and mentor junior developers to ensure code quality.",
        "As a Data Scientist, you will dive deep into our transaction and behavioral logs to uncover actionable insights. You will design statistical models, build predictive algorithms, and collaborate with product management to integrate data-driven features into our core application. Experience with Python, SQL, and Pandas is required.",
        "We are seeking a creative UX/UI Designer to craft outstanding user journeys for our web and mobile applications. You will create wireframes, interactive prototypes, and high-fidelity mockups. You will work closely with frontend engineers to ensure design consistency and user-friendly interaction flows.",
        "Join our engineering team as a DevOps Engineer. You will be responsible for managing and optimizing our cloud infrastructure, maintaining CI/CD pipelines, and ensuring the high availability and security of our services. Experience with AWS, Docker, and Kubernetes is highly preferred."
    ]
    
    fake_descriptions = [
        "Urgent Help Needed! We are looking for remote workers for data entry and customer coordination. Work from home in your spare time, just 2-3 hours per day. High income potential: earn up to $3000 to $5000 weekly! No experience is required, full training is provided. Apply today and start immediately. Fast payouts via wire transfer or check.",
        "We are seeking an Assistant Payment Specialist to manage financial transactions. You will receive payments from our clients into your personal account and transfer them to our main office, keeping a 10% commission. This is a very easy job that takes less than an hour a day. Start making money from home now!",
        "Earn Money From Home! Simple package processing and shipping position. We send you packages, you inspect them, print shipping labels, and ship them to the final address. All shipping costs are prepaid. Excellent compensation: $25 per package processed. Must have a smartphone and reliable internet connection.",
        "Urgent opening for an Online Typist. Convert scanned documents and PDFs into MS Word files. High accuracy is essential. This is a flexible remote job. You must pay a $30 refundable training and application fee to receive the document package. Earn high rates per completed page."
    ]
    
    real_requirements = [
        "Bachelor's degree in Computer Science, engineering, or a related field. 3+ years of experience with Python or Java. Strong understanding of database systems (SQL and NoSQL). Excellent communication and teamwork skills.",
        "Degree in Statistics, Mathematics, or Data Science. Proficiency in Python (NumPy, Pandas, Scipy) and SQL. Experience with machine learning libraries like Scikit-Learn. Ability to communicate technical findings to stakeholders.",
        "Proven experience as a UX/UI Designer with a strong portfolio. Proficiency in Figma, Sketch, or Adobe XD. Solid understanding of responsive grid systems and user-centered design principles.",
        "Strong experience managing AWS cloud services. Proficient with Git, Docker, Jenkins or GitHub Actions. Solid scripting skills in Bash or Python. Understanding of networking and system security."
    ]
    
    fake_requirements = [
        "Must have a computer or smartphone with internet access. Ability to work independently with minimal supervision. No prior experience required. Must have an active bank account to receive direct deposits. Must be at least 18 years old.",
        "Must be detail-oriented and quick to respond to email instructions. Access to online banking is a must for swift transfers. High school diploma or equivalent. No special skills needed, we train you in 1 hour.",
        "Reliable internet connection and basic typing skills. Ability to follow instructions carefully. Must have a valid ID. Must be ready to start immediately.",
        "No education requirements. Basic knowledge of MS Word. Energetic and willing to work part-time. Must pay the refundable registration fee to verify identity."
    ]
    
    real_benefits = [
        "Competitive salary with performance bonuses. Comprehensive health, dental, and vision insurance. Flexible working hours and remote options. 401(k) retirement matching. Continuous learning budget and training.",
        "Health benefits, paid time off, and stock options. Modern office with snacks and game room. Remote work budget. Annual company retreats.",
        "Flexible working hours, fully remote environment. Equipment stipend (MacBook + Monitor). Health insurance and wellness allowance.",
        "Competitive package. Paid sick leave and family leave. Free gym membership and transit subsidy. Career progression programs."
    ]
    
    fake_benefits = [
        "High payout, flexible hours, work from anywhere. Weekly cash payouts, direct deposit, huge sign-on bonus.",
        "Earn up to $500 per day. Work at your own pace. 10% cash commission on every transaction processed immediately.",
        "Work from home, choose your own hours. Quick advancement opportunity. Guaranteed weekly payments.",
        "Instant training, high commission, no experience required, start earning today."
    ]
    
    employment_types = ["Full-time", "Part-time", "Contract", "Temporary", "Other"]
    experiences = ["Entry level", "Associate", "Mid-Senior level", "Director", "Executive", "Internship", "Not Applicable"]
    educations = ["Bachelor's Degree", "Master's Degree", "High School Coursework", "Associate Degree", "Doctorate", "Unspecified"]
    industries = ["Information Technology", "Financial Services", "Marketing & Advertising", "Health Care", "Education", "Retail", "Human Resources"]
    functions = ["Engineering", "Sales", "Marketing", "Customer Service", "Administrative", "Finance", "Consulting"]
    
    records = []
    
    # Generate 320 Real Jobs
    for i in range(1, 321):
        job_id = i
        title = random.choice(real_titles)
        loc = random.choice(locations)
        dept = random.choice(departments)
        
        salary_min = random.choice([40, 50, 60, 80, 100])
        salary_max = salary_min + random.choice([15, 20, 30, 40])
        salary_range = f"{salary_min}000-{salary_max}000"
        
        profile = random.choice(real_profiles)
        desc = random.choice(real_descriptions)
        req = random.choice(real_requirements)
        ben = random.choice(real_benefits)
        
        telecommuting = random.choice([0, 0, 0, 1]) # 25% remote
        has_company_logo = random.choice([1, 1, 1, 0]) # 75% has logo
        has_questions = random.choice([0, 1])
        
        employment = random.choice(employment_types[:3]) # Full-time, Part-time, Contract
        exp = random.choice(experiences[:4]) # Entry, Associate, Mid-Senior, Director
        edu = random.choice(educations[:3]) # Bachelors, Masters, High school
        ind = random.choice(industries)
        func = random.choice(functions)
        
        records.append([
            job_id, title, loc, dept, salary_range, profile, desc, req, ben,
            telecommuting, has_company_logo, has_questions, employment,
            exp, edu, ind, func, 0
        ])
        
    # Generate 80 Fake Jobs (scams)
    for i in range(321, 401):
        job_id = i
        title = random.choice(fake_titles)
        loc = random.choice(locations)
        dept = random.choice(["", "Administrative", "Financial", "Operations"])
        
        salary_min = random.choice([15, 25, 35, 50])
        salary_max = salary_min + random.choice([10, 15, 25, 50])
        # Sometimes unrealistic salary formats or extremely high part-time pay
        salary_range = f"{salary_min}00-{salary_max}00" if random.random() > 0.5 else f"{salary_min}0000-{salary_max}0000"
        
        profile = random.choice(fake_profiles)
        desc = random.choice(fake_descriptions)
        req = random.choice(fake_requirements)
        ben = random.choice(fake_benefits)
        
        telecommuting = random.choice([1, 1, 0]) # 66% remote
        has_company_logo = random.choice([0, 0, 1]) # 66% no logo
        has_questions = random.choice([0, 0, 0, 1]) # mostly no questions
        
        employment = random.choice(employment_types)
        exp = random.choice(experiences)
        edu = random.choice(educations)
        ind = random.choice(industries)
        func = random.choice(functions)
        
        records.append([
            job_id, title, loc, dept, salary_range, profile, desc, req, ben,
            telecommuting, has_company_logo, has_questions, employment,
            exp, edu, ind, func, 1
        ])
        
    # Shuffle dataset
    random.shuffle(records)
    
    # Save to CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(records)
        
    print(f"Dataset generated at {filepath} with {len(records)} records.")

if __name__ == '__main__':
    generate_dataset()
