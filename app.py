import os
import sqlite3
import datetime
import threading
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd

# Import local machine learning scripts
from model.predictor import JobPredictor
from model.pipeline import train_and_evaluate

app = Flask(__name__)
app.secret_key = 'fake_job_detection_secret_key_2026'
DATABASE = os.path.join('database', 'database.db')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs('database', exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Predictor instance (loaded lazily on demand)
_predictor = None
predictor_lock = threading.Lock()

def get_predictor():
    global _predictor
    with predictor_lock:
        if _predictor is None:
            _predictor = JobPredictor()
        return _predictor

# Thread safety variables for model retraining
retraining_lock = threading.Lock()
is_retraining = False
retrain_message = ""

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create Predictions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_title TEXT NOT NULL,
            company_name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            requirements TEXT,
            benefits TEXT,
            employment_type TEXT,
            salary_info TEXT,
            prediction_result INTEGER NOT NULL,
            confidence_score REAL NOT NULL,
            explanation TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    ''')
    
    # Create Uploaded Datasets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploaded_datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            row_count INTEGER NOT NULL,
            uploaded_by TEXT NOT NULL,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Preseed Admin and User accounts
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_admin_password = generate_password_hash("admin123")
        cursor.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ("admin", "admin@fakejobs.com", hashed_admin_password, 1)
        )
        
    cursor.execute("SELECT * FROM users WHERE username = 'user'")
    if not cursor.fetchone():
        hashed_user_password = generate_password_hash("password123")
        cursor.execute(
            "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ("user", "user@example.com", hashed_user_password, 0)
        )
        
    conn.commit()
    conn.close()

init_db()

# Middleware to load user session
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()

# Authentication Decorators
def login_required(view):
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    import functools
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please log in as Admin.", "warning")
            return redirect(url_for('login'))
        if not g.user['is_admin']:
            flash("Unauthorized. Admin access required.", "danger")
            return redirect(url_for('dashboard'))
        return view(**kwargs)
    return wrapped_view

# File uploads checker
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------- ROUTES -----------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not email or not password:
            flash("All fields are required.", "danger")
            return render_template('register.html')
            
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template('register.html')
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if username or email exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            flash("Username or Email already registered.", "danger")
            conn.close()
            return render_template('register.html')
            
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
            flash("Registration successful! You can now log in.", "success")
            conn.close()
            return redirect(url_for('login'))
        except Exception as e:
            conn.close()
            flash(f"Error during registration: {e}", "danger")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        if not username or not password:
            flash("Please enter both username and password.", "danger")
            return render_template('login.html')
            
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = bool(user['is_admin'])
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    # Stats
    total_predictions = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id = ?", (g.user['id'],)
    ).fetchone()[0]
    
    fake_predictions = conn.execute(
        "SELECT COUNT(*) FROM predictions WHERE user_id = ? AND prediction_result = 1", (g.user['id'],)
    ).fetchone()[0]
    
    real_predictions = total_predictions - fake_predictions
    
    # Recent predictions
    recent_predictions = conn.execute(
        "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (g.user['id'],)
    ).fetchall()
    
    conn.close()
    
    # Loading ML Training stats
    ml_report = None
    if os.path.exists(os.path.join('trained_model', 'training_report.json')):
        try:
            import json
            with open(os.path.join('trained_model', 'training_report.json'), 'r') as f:
                ml_report = json.load(f)
        except Exception:
            pass
            
    return render_template(
        'dashboard.html',
        total_predictions=total_predictions,
        fake_predictions=fake_predictions,
        real_predictions=real_predictions,
        recent_predictions=recent_predictions,
        ml_report=ml_report
    )

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    if request.method == 'POST':
        job_data = {
            'title': request.form.get('title', '').strip(),
            'company_name': request.form.get('company_name', '').strip(),
            'location': request.form.get('location', '').strip(),
            'department': request.form.get('department', '').strip(),
            'description': request.form.get('description', '').strip(),
            'requirements': request.form.get('requirements', '').strip(),
            'benefits': request.form.get('benefits', '').strip(),
            'employment_type': request.form.get('employment_type', ''),
            'required_experience': request.form.get('required_experience', ''),
            'required_education': request.form.get('required_education', ''),
            'industry': request.form.get('industry', '').strip(),
            'function': request.form.get('function', '').strip(),
            'salary_info': request.form.get('salary_info', '').strip()
        }
        
        # Validation
        if not job_data['title'] or not job_data['description']:
            flash("Job Title and Job Description are required fields.", "danger")
            return render_template('predict.html')
            
        try:
            predictor = get_predictor()
            result = predictor.predict(job_data)
            
            # Save prediction to database
            conn = get_db_connection()
            conn.execute('''
                INSERT INTO predictions (
                    user_id, job_title, company_name, location, description, 
                    requirements, benefits, employment_type, salary_info, 
                    prediction_result, confidence_score, explanation
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                g.user['id'], job_data['title'], job_data['company_name'], job_data['location'],
                job_data['description'], job_data['requirements'], job_data['benefits'],
                job_data['employment_type'], job_data['salary_info'],
                result['label'], result['confidence'], result['explanation']
            ))
            conn.commit()
            conn.close()
            flash("Prediction executed successfully!", "success")
        except Exception as e:
            flash(f"Error executing prediction: {e}", "danger")
            
    return render_template('predict.html', result=result)

@app.route('/analytics')
@login_required
def analytics():
    # Load ML Accuracy report data
    ml_report = None
    if os.path.exists(os.path.join('trained_model', 'training_report.json')):
        try:
            import json
            with open(os.path.join('trained_model', 'training_report.json'), 'r') as f:
                ml_report = json.load(f)
        except Exception:
            pass
            
    return render_template('analytics.html', ml_report=ml_report)

# AJAX data endpoints for charts
@app.route('/api/predictions_stats')
@login_required
def api_predictions_stats():
    conn = get_db_connection()
    # 1. Total real vs fake predictions
    counts = conn.execute('''
        SELECT prediction_result, COUNT(*) as count 
        FROM predictions 
        GROUP BY prediction_result
    ''').fetchall()
    
    real_count = 0
    fake_count = 0
    for row in counts:
        if row['prediction_result'] == 0:
            real_count = row['count']
        elif row['prediction_result'] == 1:
            fake_count = row['count']
            
    # 2. Monthly predictions trend (grouped by YYYY-MM)
    monthly = conn.execute('''
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
        FROM predictions
        GROUP BY month
        ORDER BY month ASC
        LIMIT 12
    ''').fetchall()
    
    months_labels = [row['month'] for row in monthly]
    months_counts = [row['count'] for row in monthly]
    
    # 3. User distribution
    user_preds = conn.execute('''
        SELECT u.username, COUNT(p.id) as count
        FROM users u
        LEFT JOIN predictions p ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY count DESC
        LIMIT 5
    ''').fetchall()
    user_labels = [row['username'] for row in user_preds]
    user_counts = [row['count'] for row in user_preds]
    
    conn.close()
    
    return jsonify({
        'pie_data': [real_count, fake_count],
        'monthly_labels': months_labels if months_labels else [datetime.datetime.now().strftime('%Y-%m')],
        'monthly_counts': months_counts if months_counts else [0],
        'user_labels': user_labels,
        'user_counts': user_counts
    })

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip()
    filter_type = request.args.get('type', 'all')
    
    conn = get_db_connection()
    sql = "SELECT * FROM predictions WHERE user_id = ?"
    params = [g.user['id']]
    
    if query:
        sql += " AND (job_title LIKE ? OR company_name LIKE ? OR location LIKE ? OR description LIKE ?)"
        term = f"%{query}%"
        params.extend([term, term, term, term])
        
    if filter_type == 'real':
        sql += " AND prediction_result = 0"
    elif filter_type == 'fake':
        sql += " AND prediction_result = 1"
        
    sql += " ORDER BY created_at DESC"
    predictions_list = conn.execute(sql, params).fetchall()
    conn.close()
    
    return render_template('search.html', predictions=predictions_list, query=query, filter_type=filter_type)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            email = request.form.get('email', '').strip()
            if not email:
                flash("Email cannot be empty.", "danger")
            else:
                conn = get_db_connection()
                try:
                    conn.execute("UPDATE users SET email = ? WHERE id = ?", (email, g.user['id']))
                    conn.commit()
                    flash("Profile updated successfully.", "success")
                except Exception as e:
                    flash(f"Error updating email: {e}", "danger")
                finally:
                    conn.close()
            return redirect(url_for('profile'))
            
        elif action == 'change_password':
            old_password = request.form.get('old_password')
            new_password = request.form.get('new_password')
            confirm_new = request.form.get('confirm_new')
            
            if not old_password or not new_password:
                flash("Please fill in all password fields.", "danger")
                return redirect(url_for('profile'))
                
            if new_password != confirm_new:
                flash("New passwords do not match.", "danger")
                return redirect(url_for('profile'))
                
            if not check_password_hash(g.user['password'], old_password):
                flash("Incorrect current password.", "danger")
                return redirect(url_for('profile'))
                
            conn = get_db_connection()
            try:
                hashed = generate_password_hash(new_password)
                conn.execute("UPDATE users SET password = ? WHERE id = ?", (hashed, g.user['id']))
                conn.commit()
                flash("Password changed successfully.", "success")
            except Exception as e:
                flash(f"Error updating password: {e}", "danger")
            finally:
                conn.close()
            return redirect(url_for('profile'))
            
        elif action == 'delete_account':
            conn = get_db_connection()
            try:
                # Delete predictions first or let cascade handle it. SQLite checks:
                conn.execute("DELETE FROM predictions WHERE user_id = ?", (g.user['id'],))
                conn.execute("DELETE FROM users WHERE id = ?", (g.user['id'],))
                conn.commit()
                session.clear()
                flash("Your account has been deleted permanently.", "success")
                conn.close()
                return redirect(url_for('index'))
            except Exception as e:
                conn.close()
                flash(f"Error deleting account: {e}", "danger")
                return redirect(url_for('profile'))
                
    return render_template('profile.html')

# ----------------- ADMIN ROUTES -----------------

@app.route('/admin')
@admin_required
def admin():
    conn = get_db_connection()
    
    # Users
    users_list = conn.execute("SELECT id, username, email, is_admin, created_at FROM users ORDER BY created_at DESC").fetchall()
    
    # System Stats
    total_users = len(users_list)
    total_preds = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    
    fake_preds = conn.execute("SELECT COUNT(*) FROM predictions WHERE prediction_result = 1").fetchone()[0]
    fake_ratio = round((fake_preds / total_preds * 100), 2) if total_preds > 0 else 0
    
    # Previous predictions
    all_predictions = conn.execute('''
        SELECT p.*, u.username 
        FROM predictions p 
        LEFT JOIN users u ON p.user_id = u.id 
        ORDER BY p.created_at DESC
    ''').fetchall()
    
    # Uploaded datasets
    datasets = conn.execute("SELECT * FROM uploaded_datasets ORDER BY uploaded_at DESC").fetchall()
    
    conn.close()
    
    # Best model config
    ml_report = None
    if os.path.exists(os.path.join('trained_model', 'training_report.json')):
        try:
            import json
            with open(os.path.join('trained_model', 'training_report.json'), 'r') as f:
                ml_report = json.load(f)
        except Exception:
            pass
            
    global is_retraining, retrain_message
    return render_template(
        'admin.html',
        users=users_list,
        total_users=total_users,
        total_predictions=total_preds,
        fake_ratio=fake_ratio,
        predictions=all_predictions,
        datasets=datasets,
        ml_report=ml_report,
        is_retraining=is_retraining,
        retrain_message=retrain_message
    )

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == g.user['id']:
        flash("You cannot delete your own admin account.", "danger")
        return redirect(url_for('admin'))
        
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM predictions WHERE user_id = ?", (user_id,))
        conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        flash("User and their predictions deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting user: {e}", "danger")
    finally:
        conn.close()
        
    return redirect(url_for('admin'))

def background_retrain(secure_path, original_filename, username):
    global is_retraining, retrain_message, _predictor
    with retraining_lock:
        is_retraining = True
        retrain_message = "Validating and parsing CSV file..."
        
    try:
        # Load the uploaded dataset
        new_df = pd.read_csv(secure_path)
        
        # Validate columns
        required_cols = ['title', 'description', 'fraudulent']
        missing_cols = [col for col in required_cols if col not in new_df.columns]
        
        if missing_cols:
            raise ValueError(f"Uploaded CSV is missing mandatory columns: {', '.join(missing_cols)}")
            
        with retraining_lock:
            retrain_message = "Merging new rows with master dataset..."
            
        master_path = os.path.join('dataset', 'fake_job_postings.csv')
        master_df = pd.read_csv(master_path)
        
        # Ensure we keep the exact columns as master
        for col in master_df.columns:
            if col not in new_df.columns:
                new_df[col] = ""
                
        # Filter columns to match master schema
        new_df = new_df[master_df.columns]
        
        # Clean data types
        new_df['job_id'] = range(len(master_df) + 1, len(master_df) + len(new_df) + 1)
        new_df['fraudulent'] = new_df['fraudulent'].fillna(0).astype(int)
        
        # Append to master dataset
        combined_df = pd.concat([master_df, new_df], ignore_index=True)
        combined_df.to_csv(master_path, index=False)
        
        # Record upload in Database
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO uploaded_datasets (filename, row_count, uploaded_by) VALUES (?, ?, ?)",
            (original_filename, len(new_df), username)
        )
        conn.commit()
        conn.close()
        
        with retraining_lock:
            retrain_message = "Comparing and retraining models (this may take up to a minute)..."
            
        # Run training pipeline
        train_and_evaluate(master_path)
        
        # Reset predictor model in-memory
        with predictor_lock:
            _predictor = None # Will reload from new .pkl files next predict request
            
        with retraining_lock:
            is_retraining = False
            retrain_message = "Retraining complete! Best model selected and updated successfully."
            
    except Exception as e:
        with retraining_lock:
            is_retraining = False
            retrain_message = f"Error during retraining: {str(e)}"

@app.route('/admin/upload_csv', methods=['POST'])
@admin_required
def upload_csv():
    global is_retraining
    if is_retraining:
        flash("A retraining process is currently running. Please wait.", "warning")
        return redirect(url_for('admin'))
        
    if 'file' not in request.files:
        flash("No file part in request.", "danger")
        return redirect(url_for('admin'))
        
    file = request.files['file']
    if file.filename == '':
        flash("No file selected.", "danger")
        return redirect(url_for('admin'))
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_filename = f"{timestamp}_{filename}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_filename)
        file.save(save_path)
        
        # Launch retraining as a background task to prevent request timeouts
        thread = threading.Thread(
            target=background_retrain,
            args=(save_path, filename, g.user['username'])
        )
        thread.start()
        
        flash("Dataset uploaded successfully! Model retraining has started in the background. Refresh this page to track progress.", "success")
    else:
        flash("Invalid file format. Only CSV files are allowed.", "danger")
        
    return redirect(url_for('admin'))

@app.route('/admin/retrain_status')
@admin_required
def retrain_status():
    global is_retraining, retrain_message
    return jsonify({
        'is_retraining': is_retraining,
        'message': retrain_message
    })

if __name__ == '__main__':
    app.run(debug=True)
