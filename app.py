#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# COMMUNITY ENGAGEMENT PLATFORM - Complete Working Code
# Run this entire cell to start the application

import sqlite3
import datetime
import os
import uuid
import json
from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'citizen_engagement_secret_key_2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx', 'txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

DATABASE = 'citizens.db'

# ============================================
# MULTI-LANGUAGE SUPPORT (4 Languages)
# ============================================

T = {
    'kin': {
        'app_title': 'ITORERO RYABATURAGE', 'nav_submit': 'Tanga Ikibazo', 'nav_track': 'Kurikira',
        'nav_login': 'Kwinjira', 'submit_issue': 'TANGA IKIBAZO', 'your_voice': 'Ijwi ryawe rirakwiye!',
        'full_name': 'Izina Riryaje', 'email': 'E-mail', 'phone': 'Telefone', 'title': 'Umutwe',
        'description': 'Ibisobanuro', 'category': 'Icyiciro', 'priority': 'Ubwitonzi', 'location': 'Aho uherereye',
        'low': 'Gake', 'medium': 'Hagati', 'high': 'Nyinshi', 'submit_btn': 'Ohereza', 'quick_response': 'Igisubizo Vuba',
        'find_issues': 'Shakira Ibibazo', 'enter_email': 'Andika email', 'search': 'Shakisha', 'my_issues': 'Ibibazo Byanjye',
        'no_issues': 'Nta kibazo', 'login': 'Kwinjira', 'email_label': 'E-mail', 'password_label': 'Ijambobanga',
        'login_btn': 'Injira', 'status': 'Ihame', 'actions': 'Ibikorwa', 'approve': 'Emera', 'reject': 'Janga',
        'view': 'Reba', 'total_issues': 'Ibibazo Byose', 'pending': 'Bitegereje', 'id': 'INDANGAMUNTU', 'citizen': 'Umuturage',
        'select_language': 'Hitamo Ururimi', 'welcome': 'Murakaza neza', 'comment_added': 'Igitekerezo cyongewe!',
        'issue_submitted': 'Ikibazo cyatanzwe!', 'error_occurred': 'Habaye ikibazo', 'invalid_creds': 'Amakuru atari yo',
        'thank_you': 'Urakoze'
    },
    'en': {
        'app_title': 'COMMUNITY ENGAGEMENT PLATFORM', 'nav_submit': 'Submit Issue', 'nav_track': 'Track',
        'nav_login': 'Login', 'submit_issue': 'REPORT AN ISSUE', 'your_voice': 'Your voice matters!',
        'full_name': 'Full Name', 'email': 'Email', 'phone': 'Phone Number', 'title': 'Title',
        'description': 'Description', 'category': 'Category', 'priority': 'Priority', 'location': 'Location',
        'low': 'Low', 'medium': 'Medium', 'high': 'High', 'submit_btn': 'Submit', 'quick_response': 'Quick Response',
        'find_issues': 'Find Issues', 'enter_email': 'Enter your email', 'search': 'Search', 'my_issues': 'My Issues',
        'no_issues': 'No issues found', 'login': 'Login', 'email_label': 'Email', 'password_label': 'Password',
        'login_btn': 'Login', 'status': 'Status', 'actions': 'Actions', 'approve': 'Approve', 'reject': 'Reject',
        'view': 'View', 'total_issues': 'Total Issues', 'pending': 'Pending', 'id': 'ID', 'citizen': 'Citizen',
        'select_language': 'Select Language', 'welcome': 'Welcome', 'comment_added': 'Comment added!',
        'issue_submitted': 'Issue submitted!', 'error_occurred': 'Error occurred', 'invalid_creds': 'Invalid credentials',
        'thank_you': 'Thank you'
    },
    'fr': {
        'app_title': 'PLATEFORME CITOYENNE', 'nav_submit': 'Soumettre', 'nav_track': 'Suivre',
        'nav_login': 'Connexion', 'submit_issue': 'SIGNALER UN PROBLÈME', 'your_voice': 'Votre voix compte!',
        'full_name': 'Nom Complet', 'email': 'E-mail', 'phone': 'Téléphone', 'title': 'Titre',
        'description': 'Description', 'category': 'Catégorie', 'priority': 'Priorité', 'location': 'Lieu',
        'low': 'Basse', 'medium': 'Moyenne', 'high': 'Haute', 'submit_btn': 'Soumettre', 'quick_response': 'Réponse Rapide',
        'find_issues': 'Trouver', 'enter_email': 'Entrez votre email', 'search': 'Rechercher', 'my_issues': 'Mes Problèmes',
        'no_issues': 'Aucun problème', 'login': 'Connexion', 'email_label': 'Email', 'password_label': 'Mot de passe',
        'login_btn': 'Se connecter', 'status': 'Statut', 'actions': 'Actions', 'approve': 'Approuver', 'reject': 'Rejeter',
        'view': 'Voir', 'total_issues': 'Total', 'pending': 'En attente', 'id': 'ID', 'citizen': 'Citoyen',
        'select_language': 'Choisir la langue', 'welcome': 'Bienvenue', 'comment_added': 'Commentaire ajouté!',
        'issue_submitted': 'Problème soumis!', 'error_occurred': 'Erreur', 'invalid_creds': 'Identifiants invalides',
        'thank_you': 'Merci'
    },
    'sw': {
        'app_title': 'JUKWAA LA JAMII', 'nav_submit': 'Wasilisha', 'nav_track': 'Fuatilia',
        'nav_login': 'Ingia', 'submit_issue': 'WASILISHA SUALA', 'your_voice': 'Sauti yako ina maana!',
        'full_name': 'Jina Kamili', 'email': 'Barua pepe', 'phone': 'Nambari ya Simu', 'title': 'Kichwa',
        'description': 'Maelezo', 'category': 'Kategoria', 'priority': 'Kipaumbele', 'location': 'Eneo',
        'low': 'Chini', 'medium': 'Kati', 'high': 'Juu', 'submit_btn': 'Wasilisha', 'quick_response': 'Majibu ya Haraka',
        'find_issues': 'Tafuta Masuala', 'enter_email': 'Weka barua pepe', 'search': 'Tafuta', 'my_issues': 'Masuala Yangu',
        'no_issues': 'Hakuna masuala', 'login': 'Ingia', 'email_label': 'Barua pepe', 'password_label': 'Nywila',
        'login_btn': 'Ingia', 'status': 'Hali', 'actions': 'Vitendo', 'approve': 'Idhinisha', 'reject': 'Kataa',
        'view': 'Angalia', 'total_issues': 'Jumla ya Masuala', 'pending': 'Inasubiri', 'id': 'KITAMBULISHO', 'citizen': 'Rai',
        'select_language': 'Chagua Lugha', 'welcome': 'Karibu', 'comment_added': 'Maoni yameongezwa!',
        'issue_submitted': 'Suala limewasilishwa!', 'error_occurred': 'Hitilafu', 'invalid_creds': 'Vitambulisho si sahihi',
        'thank_you': 'Asante'
    }
}

LANGUAGE_SELECTOR = '''
<div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: white; padding: 5px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
    <select onchange="changeLanguage(this.value)" style="padding: 8px 12px; border-radius: 5px; border: 1px solid #667eea; background: white; cursor: pointer; font-weight: bold;">
        <option value="kin" {% if session.lang == 'kin' %}selected{% endif %}>🇷🇼 Kinyarwanda</option>
        <option value="en" {% if session.lang == 'en' %}selected{% endif %}>🇬🇧 English</option>
        <option value="fr" {% if session.lang == 'fr' %}selected{% endif %}>🇫🇷 Français</option>
        <option value="sw" {% if session.lang == 'sw' %}selected{% endif %}>🇹🇿 Kiswahili</option>
    </select>
</div>
<script>
function changeLanguage(lang) {
    fetch('/set_language/' + lang).then(r=>r.json()).then(data=>{if(data.success) location.reload();});
}
</script>
'''

def get_text(key):
    lang = session.get('lang', 'en')
    return T.get(lang, T['en']).get(key, key)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        citizen_name TEXT NOT NULL,
        citizen_email TEXT NOT NULL,
        citizen_phone TEXT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        priority TEXT DEFAULT 'medium',
        admin_status TEXT DEFAULT 'pending',
        admin_feedback TEXT,
        created_date TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS leaders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        region TEXT NOT NULL,
        role TEXT NOT NULL,
        approval_status TEXT DEFAULT 'approved',
        created_date TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER NOT NULL,
        user_name TEXT NOT NULL,
        comment TEXT NOT NULL,
        created_date TEXT NOT NULL
    )''')

    admin = c.execute("SELECT * FROM leaders WHERE email='admin@community.com'").fetchone()
    if not admin:
        c.execute("INSERT INTO leaders (name, email, password, region, role, created_date) VALUES (?,?,?,?,?,?)",
                  ('System Admin', 'admin@community.com', 'admin123', 'All Regions', 'admin',
                   datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()
    print("Database initialized!")
    print("Admin: admin@community.com / admin123")

init_db()

# ============================================
# HTML TEMPLATES
# ============================================

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head><title>{{ get_text('app_title') }}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;}
.container{max-width:1200px;margin:0 auto;padding:20px;}
header{background:white;border-radius:10px;padding:20px;margin-bottom:30px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
h1{color:#667eea;}
nav{display:flex;gap:20px;margin-top:20px;padding-top:15px;border-top:1px solid #ddd;flex-wrap:wrap;}
nav a{text-decoration:none;color:#666;padding:8px16px;border-radius:5px;}
nav a:hover{background:#667eea;color:white;}
main{background:white;border-radius:10px;padding:30px;box-shadow:0 2px 10px rgba(0,0,0,0.1);}
.form-container{max-width:800px;margin:0 auto;}
.form-section{margin-bottom:30px;padding:20px;background:#f8f9fa;border-radius:8px;}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:15px;}
.form-group{margin-bottom:15px;}
.form-group label{display:block;margin-bottom:8px;font-weight:bold;}
.form-group input,.form-group textarea,.form-group select{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;}
.btn-submit{background:#667eea;color:white;border:none;padding:12px;border-radius:5px;cursor:pointer;width:100%;font-size:16px;}
.btn-submit:hover{background:#764ba2;}
.alert{padding:12px;border-radius:5px;margin-bottom:20px;}
.alert-success{background:#d4edda;color:#155724;}
.alert-error{background:#f8d7da;color:#721c24;}
.phone-hint{font-size:11px;color:#999;margin-top:3px;}
</style>
</head>
<body>{{ language_selector|safe }}
<div class="container">
<header><h1>🏘️ {{ get_text('app_title') }}</h1><p>Empowering Communities</p>
<nav><a href="/">{{ get_text('nav_submit') }}</a><a href="/search_issues">{{ get_text('nav_track') }}</a><a href="/login">{{ get_text('nav_login') }}</a></nav></header>
<main>
{% with messages = get_flashed_messages(with_categories=true) %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endwith %}
<div class="form-container">
<h2 style="text-align:center;color:#667eea;margin-bottom:20px;">{{ get_text('submit_issue') }}</h2>
<p style="text-align:center;margin-bottom:30px;">{{ get_text('your_voice') }}</p>
<form action="/submit_issue" method="POST">
<div class="form-section"><h3>{{ get_text('full_name') }}</h3>
<div class="form-row"><div class="form-group"><label>{{ get_text('full_name') }}</label><input type="text" name="citizen_name" required></div>
<div class="form-group"><label>{{ get_text('email') }}</label><input type="email" name="citizen_email" required></div></div>
<div class="form-group"><label>{{ get_text('phone') }}</label>
<input type="tel" name="citizen_phone" placeholder="e.g., 0788123456">
<div class="phone-hint">📱 You will receive updates on this number</div>
</div></div>
<div class="form-section"><h3>Issue Details</h3>
<div class="form-group"><label>{{ get_text('title') }}</label><input type="text" name="title" required></div>
<div class="form-group"><label>{{ get_text('description') }}</label><textarea name="description" rows="5" required></textarea></div>
<div class="form-row"><div class="form-group"><label>{{ get_text('category') }}</label><select name="category"><option>Infrastructure</option><option>Sanitation</option><option>Water</option><option>Electricity</option><option>Healthcare</option></select></div>
<div class="form-group"><label>{{ get_text('priority') }}</label><select name="priority"><option value="low">{{ get_text('low') }}</option><option value="medium" selected>{{ get_text('medium') }}</option><option value="high">{{ get_text('high') }}</option></select></div></div>
<div class="form-group"><label>{{ get_text('location') }}</label><input type="text" name="location" required></div></div>
<button type="submit" class="btn-submit">{{ get_text('submit_btn') }}</button></form></div></main></div></body></html>
'''

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['kin', 'en', 'fr', 'sw']:
        session['lang'] = lang
    return jsonify({'success': True})

@app.route('/')
def index():
    return render_template_string(INDEX_HTML, get_text=get_text, language_selector=LANGUAGE_SELECTOR)

@app.route('/submit_issue', methods=['POST'])
def submit_issue():
    try:
        conn = get_db_connection()
        conn.execute('''INSERT INTO issues (citizen_name, citizen_email, citizen_phone, title, description, category, location, priority, created_date)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                     (request.form['citizen_name'], request.form['citizen_email'], request.form.get('citizen_phone',''),
                      request.form['title'], request.form['description'], request.form['category'],
                      request.form['location'], request.form.get('priority','medium'),
                      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        issue_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        conn.commit()
        conn.close()
        flash(f'{get_text("issue_submitted")} #{issue_id}', 'success')
        return redirect(url_for('track_issue', issue_id=issue_id))
    except Exception as e:
        flash(f'{get_text("error_occurred")}: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/track/<int:issue_id>')
def track_issue(issue_id):
    conn = get_db_connection()
    issue = conn.execute('SELECT * FROM issues WHERE id = ?', (issue_id,)).fetchone()
    comments = conn.execute('SELECT * FROM comments WHERE issue_id = ? ORDER BY created_date DESC', (issue_id,)).fetchall()
    conn.close()
    if not issue:
        flash('Issue not found', 'error')
        return redirect(url_for('index'))
    return render_template_string(TRACK_HTML, issue=issue, comments=comments, get_text=get_text, language_selector=LANGUAGE_SELECTOR)

TRACK_HTML = '''
<!DOCTYPE html>
<html><head><title>Issue #{{ issue.id }}</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);}.container{max-width:1000px;margin:0 auto;padding:20px;}
header{background:white;border-radius:10px;padding:20px;margin-bottom:20px;}nav{display:flex;gap:20px;margin-top:15px;flex-wrap:wrap;}
nav a{text-decoration:none;color:#666;padding:8px16px;border-radius:5px;}nav a:hover{background:#667eea;color:white;}
main{background:white;border-radius:10px;padding:30px;}.info-box{background:#f8f9fa;padding:20px;border-radius:8px;margin-bottom:20px;}
.status{padding:4px12px;border-radius:20px;display:inline-block;}.status-pending{background:#ffc107;}.status-approved{background:#28a745;color:white;}
.status-rejected{background:#dc3545;color:white;}.btn-back{background:#667eea;color:white;padding:10px20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:20px;}
.comment-form{background:#f8f9fa;padding:20px;border-radius:8px;margin-bottom:20px;}
.comment-form input,.comment-form textarea{width:100%;padding:10px;margin-bottom:10px;border:1px solid #ddd;border-radius:5px;}
.comment-form button{background:#667eea;color:white;border:none;padding:10px20px;border-radius:5px;cursor:pointer;}
.comment-item{background:#f8f9fa;padding:15px;border-radius:8px;margin-bottom:10px;}
</style></head>
<body>{{ language_selector|safe }}
<div class="container"><header><h1>📋 Issue Details</h1><nav><a href="/">{{ get_text('nav_submit') }}</a><a href="/search_issues">{{ get_text('nav_track') }}</a><a href="/login">{{ get_text('nav_login') }}</a></nav></header>
<main><h2>{{ issue.title }}</h2>
<div class="info-box"><p><strong>ID:</strong> #{{ issue.id }}</p>
<p><strong>Status:</strong> <span class="status status-{{ issue.admin_status }}">{{ issue.admin_status }}</span></p>
<p><strong>Priority:</strong> {{ issue.priority }}</p><p><strong>Category:</strong> {{ issue.category }}</p>
<p><strong>Location:</strong> {{ issue.location }}</p><p><strong>Submitted by:</strong> {{ issue.citizen_name }} ({{ issue.citizen_email }})</p>
{% if issue.citizen_phone %}<p><strong>Phone:</strong> {{ issue.citizen_phone }}</p>{% endif %}
<p><strong>Description:</strong><br>{{ issue.description }}</p>
{% if issue.admin_feedback %}<div style="background:#d1ecf1;padding:15px;border-radius:8px;margin-top:15px;"><strong>📝 Admin Feedback:</strong><br>{{ issue.admin_feedback }}</div>{% endif %}</div>
<div class="comment-section"><h3>Comments</h3>
<form action="/add_comment" method="POST" class="comment-form">
<input type="hidden" name="issue_id" value="{{ issue.id }}">
<input type="text" name="user_name" placeholder="Your name" required>
<textarea name="comment" rows="3" placeholder="Share your thoughts..." required></textarea>
<button type="submit">Post Comment</button></form>
{% if comments %}{% for comment in comments %}<div class="comment-item">
<strong>{{ comment.user_name }}</strong> <small>{{ comment.created_date }}</small>
<p>{{ comment.comment }}</p></div>{% endfor %}{% endif %}</div>
<a href="javascript:history.back()" class="btn-back">← Back</a></main></div></body></html>
'''

@app.route('/search_issues')
def search_issues():
    email = request.args.get('email')
    if email:
        conn = get_db_connection()
        issues = conn.execute('SELECT * FROM issues WHERE citizen_email = ? ORDER BY created_date DESC', (email,)).fetchall()
        conn.close()
        return render_template_string(DASHBOARD_HTML, issues=issues, email=email, get_text=get_text, language_selector=LANGUAGE_SELECTOR)
    return render_template_string(SEARCH_HTML, get_text=get_text, language_selector=LANGUAGE_SELECTOR)

SEARCH_HTML = '''
<!DOCTYPE html>
<html><head><title>Track Issues</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);}.container{max-width:600px;margin:50px auto;padding:20px;}
.card{background:white;border-radius:10px;padding:30px;text-align:center;box-shadow:0 10px 30px rgba(0,0,0,0.2);}input{width:100%;padding:10px;margin:20px0;border:1px solid #ddd;border-radius:5px;}
button{padding:10px20px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer;}</style></head>
<body>{{ language_selector|safe }}
<div class="container"><div class="card"><h2>{{ get_text('find_issues') }}</h2><p>{{ get_text('enter_email') }}</p>
<form method="GET"><input type="email" name="email" placeholder="your@email.com" required><button type="submit">{{ get_text('search') }}</button></form></div></div></body></html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html><head><title>My Issues</title>
<style>body{font-family:Arial;background:#f5f5f5;}.container{max-width:1000px;margin:0 auto;padding:20px;}
header{background:white;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}nav{display:flex;gap:20px;margin-top:15px;flex-wrap:wrap;}
nav a{text-decoration:none;color:#666;padding:8px16px;border-radius:5px;}nav a:hover{background:#667eea;color:white;}
main{background:white;border-radius:10px;padding:30px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}.issue-card{border:1px solid #ddd;border-radius:8px;padding:20px;margin-bottom:20px;}
.status{padding:4px12px;border-radius:20px;font-size:12px;}.status-pending{background:#ffc107;}.status-approved{background:#28a745;color:white;}
.status-rejected{background:#dc3545;color:white;}.btn-view{background:#667eea;color:white;padding:8px16px;text-decoration:none;border-radius:5px;display:inline-block;}</style></head>
<body>{{ language_selector|safe }}
<div class="container"><header><h1>📋 {{ get_text('my_issues') }}</h1><nav><a href="/">{{ get_text('nav_submit') }}</a><a href="/search_issues" class="active">{{ get_text('nav_track') }}</a><a href="/login">{{ get_text('nav_login') }}</a></nav></header>
<main><h2>{{ get_text('my_issues') }} for {{ email }}</h2>{% if issues %}{% for issue in issues %}
<div class="issue-card"><h3>#{{ issue.id }}: {{ issue.title }}</h3>
<p><strong>Status:</strong> <span class="status status-{{ issue.admin_status }}">{{ issue.admin_status }}</span> | <strong>Priority:</strong> {{ issue.priority }}</p>
<p><strong>Submitted:</strong> {{ issue.created_date }}</p><p>{{ issue.description[:150] }}...</p>
<a href="/track/{{ issue.id }}" class="btn-view">View Details →</a></div>{% endfor %}{% else %}<p>No issues found.</p>{% endif %}</main></div></body></html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM leaders WHERE email = ? AND password = ?', (email, password)).fetchone()
        conn.close()
        if user and user['role'] == 'admin':
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        flash(get_text('invalid_creds'), 'error')
    return render_template_string(LOGIN_HTML, get_text=get_text, language_selector=LANGUAGE_SELECTOR)

LOGIN_HTML = '''
<!DOCTYPE html>
<html><head><title>Admin Login</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);}.container{max-width:500px;margin:50px auto;padding:20px;}
.card{background:white;border-radius:10px;padding:30px;box-shadow:0 10px 30px rgba(0,0,0,0.2);}h2{color:#667eea;}
.form-group{margin-bottom:20px;}label{display:block;margin-bottom:8px;}input{width:100%;padding:10px;border:1px solid #ddd;border-radius:5px;}
button{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer;}
.alert{padding:12px;border-radius:5px;margin-bottom:20px;}.alert-error{background:#f8d7da;color:#721c24;}
</style></head>
<body>{{ language_selector|safe }}
<div class="container"><div class="card"><h2>Admin Login</h2>
{% with messages = get_flashed_messages(with_categories=true) %}{% for category, message in messages %}<div class="alert alert-{{ category }}">{{ message }}</div>{% endfor %}{% endwith %}
<form method="POST"><div class="form-group"><label>Email</label><input type="email" name="email" required></div>
<div class="form-group"><label>Password</label><input type="password" name="password" required></div>
<button type="submit">Login</button></form>
<div style="margin-top:20px;padding:10px;background:#f0f0f0;border-radius:5px;"><strong>Admin Credentials:</strong><br>Email: admin@community.com<br>Password: admin123</div></div></div></body></html>
'''

@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    conn = get_db_connection()
    issues = conn.execute('SELECT * FROM issues ORDER BY created_date DESC').fetchall()
    stats = {
        'total': len(issues),
        'pending': sum(1 for i in issues if i['admin_status'] == 'pending'),
        'approved': sum(1 for i in issues if i['admin_status'] == 'approved'),
        'rejected': sum(1 for i in issues if i['admin_status'] == 'rejected')
    }
    conn.close()
    return render_template_string(ADMIN_HTML, issues=issues, stats=stats, get_text=get_text, language_selector=LANGUAGE_SELECTOR)

ADMIN_HTML = '''
<!DOCTYPE html>
<html><head><title>Admin Dashboard</title>
<style>body{font-family:Arial;background:#f5f5f5;}.container{max-width:1200px;margin:0 auto;padding:20px;}
header{background:white;border-radius:10px;padding:20px;margin-bottom:20px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}nav{display:flex;gap:20px;margin-top:15px;}
nav a{text-decoration:none;color:#666;padding:8px16px;border-radius:5px;}nav a:hover{background:#667eea;color:white;}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:30px;}
.stat-card{background:white;padding:20px;border-radius:10px;text-align:center;box-shadow:0 2px 5px rgba(0,0,0,0.1);}
.stat-value{font-size:32px;font-weight:bold;color:#667eea;}
.section{background:white;border-radius:10px;padding:20px;margin-bottom:30px;box-shadow:0 2px 5px rgba(0,0,0,0.1);}
table{width:100%;border-collapse:collapse;}
th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd;}
.btn-approve{background:#28a745;color:white;border:none;padding:5px10px;border-radius:5px;cursor:pointer;margin:2px;}
.btn-reject{background:#dc3545;color:white;border:none;padding:5px10px;border-radius:5px;cursor:pointer;margin:2px;}
.btn-view{background:#17a2b8;color:white;padding:5px10px;text-decoration:none;border-radius:5px;margin:2px;}
.status{padding:4px8px;border-radius:20px;font-size:12px;}.status-pending{background:#ffc107;}.status-approved{background:#28a745;color:white;}
</style></head>
<body>{{ language_selector|safe }}
<div class="container"><header><h1>👨‍💼 Admin Dashboard</h1><p>Welcome, {{ session.user_name }}!</p><nav><a href="/admin_dashboard">Dashboard</a><a href="/logout">Logout</a></nav></header>
<div class="stats"><div class="stat-card"><div class="stat-value">{{ stats.total }}</div><div>Total Issues</div></div>
<div class="stat-card"><div class="stat-value">{{ stats.pending }}</div><div>Pending</div></div>
<div class="stat-card"><div class="stat-value">{{ stats.approved }}</div><div>Approved</div></div>
<div class="stat-card"><div class="stat-value">{{ stats.rejected }}</div><div>Rejected</div></div></div>
<div class="section"><h2>All Issues</h2>
<div style="overflow-x:auto;">
<table>
<thead><tr><th>ID</th><th>Title</th><th>Citizen</th><th>Phone</th><th>Priority</th><th>Status</th><th>Actions</th></tr></thead>
<tbody>{% for issue in issues %}
<tr><td>#{{ issue.id }}</td><td>{{ issue.title[:40] }}{% if issue.title|length > 40 %}...{% endif %}</td>
<td>{{ issue.citizen_name }}</td><td>{% if issue.citizen_phone %}{{ issue.citizen_phone }}{% else %}-{% endif %}</td>
<td>{{ issue.priority }}</td><td><span class="status-{{ issue.admin_status }}">{{ issue.admin_status }}</span></td>
<td><button onclick="approveIssue({{ issue.id }})" class="btn-approve">Approve</button>
<button onclick="rejectIssue({{ issue.id }})" class="btn-reject">Reject</button>
<a href="/track/{{ issue.id }}" class="btn-view">View</a></td></tr>
{% endfor %}</tbody>
</table>
</div></div>
<script>
function approveIssue(id){let f=prompt("Approval feedback:");fetch(`/admin_approve_issue/${id}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:f||"Approved",action:'approve'})}).then(()=>location.reload());}
function rejectIssue(id){let f=prompt("Rejection reason:");if(f) fetch(`/admin_approve_issue/${id}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({feedback:f,action:'reject'})}).then(()=>location.reload());}
</script></div></body></html>
'''

@app.route('/admin_approve_issue/<int:issue_id>', methods=['POST'])
def admin_approve_issue(issue_id):
    if session.get('role') != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    conn = get_db_connection()
    if data.get('action') == 'approve':
        conn.execute('UPDATE issues SET admin_status = "approved", admin_feedback = ? WHERE id = ?', (data.get('feedback', ''), issue_id))
    else:
        conn.execute('UPDATE issues SET admin_status = "rejected", admin_feedback = ? WHERE id = ?', (data.get('feedback', ''), issue_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    conn = get_db_connection()
    conn.execute('INSERT INTO comments (issue_id, user_name, comment, created_date) VALUES (?,?,?,?)',
                 (request.form['issue_id'], request.form['user_name'], request.form['comment'],
                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    flash(get_text('comment_added'), 'success')
    return redirect(url_for('track_issue', issue_id=request.form['issue_id']))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

# ============================================
# RUN THE APP
# ============================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("COMMUNITY ENGAGEMENT PLATFORM")
    print("="*50)
    print("\nLocal URL: http://127.0.0.1:5000")
    print("Admin Login: http://127.0.0.1:5000/login")
    print("Email: admin@community.com")
    print("Password: admin123")
    print("\n" + "="*50)
    app.run(debug=True, port=5002, use_reloader=False)


# In[ ]:




