import os
from flask import Flask, render_template_string, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Secret key for session signing (Keep this secure in production!)
app.secret_key = os.urandom(24)

# Database Configuration (Using SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# -------------------------------------------------------------
# Database Model (User Table)
# -------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # 60 chars is the standard length for a bcrypt hash
    password_hash = db.Column(db.String(60), nullable=False)

# -------------------------------------------------------------
# HTML Templates (Inline for single-file deployment)
# -------------------------------------------------------------
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Auth System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        .container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .flash { color: red; margin-bottom: 15px; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, msg in messages %}
                    <div class="flash {{ category }}">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

# -------------------------------------------------------------
# HTML Templates (Fixed String Concatenation)
# -------------------------------------------------------------
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Auth System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        .container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .flash { color: red; margin-bottom: 15px; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, msg in messages %}
                    <div class="flash {{ category }}">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {% block content %}{% endblock %}
    </div>
</body>
</html>
"""

LOGIN_REGISTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Auth System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        .container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; margin: 10px 0; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .flash { color: red; margin-bottom: 15px; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, msg in messages %}
                    <div class="flash {{ category }}">{{ msg }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <h2>{{ title }}</h2>
        <form method="POST">
            <label>Username</label>
            <input type="text" name="username" required autocomplete="off">
            <label>Password</label>
            <input type="password" name="password" required>
            <button type="submit">{{ title }}</button>
        </form>
        <p style="margin-top:15px;">
            {% if title == "Login" %}
                Don't have an account? <a href="/register">Register here</a>.
            {% else %}
                Already have an account? <a href="/login">Login here</a>.
            {% endif %}
        </p>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Auth System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; }
        .container { max-width: 400px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ username }}!</h2>
        <p>You have successfully logged into the secure system.</p>
        <hr>
        <a href="/logout"><button style="background-color: #DC3545;">Logout</button></a>
    </div>
</body>
</html>
"""

# -------------------------------------------------------------
# Routes & Controllers
# -------------------------------------------------------------

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Basic Input Validation
        if not username or not password:
            flash("Username and password cannot be empty.", "error")
            return render_template_string(LOGIN_REGISTER_TEMPLATE, title="Register")
        
        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template_string(LOGIN_REGISTER_TEMPLATE, title="Register")

        # Check if user already exists
        # Using SQLAlchemy ORM parameterized queries natively prevents SQL Injection
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Choose another.", "error")
            return render_template_string(LOGIN_REGISTER_TEMPLATE, title="Register")

        # Password Hashing using bcrypt
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template_string(LOGIN_REGISTER_TEMPLATE, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Secure query execution (SQL Injection safe)
        user = User.query.filter_by(username=username).first()

        # Check user existence and verify the bcrypt hash safely
        if user and bcrypt.check_password_hash(user.password_hash, password):
            # Session Management initiation
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "error")

    return render_template_string(LOGIN_REGISTER_TEMPLATE, title="Login")


@app.route('/dashboard')
def dashboard():
    # Session access control check
    if 'user_id' not in session:
        flash("Please log in to access this page.", "error")
        return redirect(url_for('login'))
    
    return render_template_string(DASHBOARD_TEMPLATE, username=session['username'])


@app.route('/logout')
def logout():
    # Clear the session data entirely
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# -------------------------------------------------------------
# App Initialization
# -------------------------------------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Generates database file and tables if they don't exist
    app.run(debug=True)
