from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)  # Added username
    phone = db.Column(db.String(20), unique=True, nullable=False)  # Added phone
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256') 

        new_user = User(username=username, phone=phone, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

    return render_template('login.html')


# Dashboard (Protected Route)
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', email=current_user.email)

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()  
    app.run(debug=True)
    
# Operational Error: qlalchemy.exc.OperationalError: (sqlite3.OperationalError) table user has no column named username
# [SQL: INSERT INTO user (username, phone, email, password) VALUES (?, ?, ?, ?)] [parameters: ('Nuhayd Shaik', '8904445302', 'sdasdn@gmail.com', 'pbkdf2:sha256:600000$IQ3XquqTcQsF17yY$0274ce17596bbb17f98d68a1d642a20aca9fc5925081d3674eedb5ded9f1ad06')]
# (Background on this error at: https://sqlalche.me/e/20/e3q8)
# Traceback (most recent call last)

