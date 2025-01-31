from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
import pandas as pd
import json,os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration Form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    phone = StringField(validators=[InputRequired(), Length(min=10, max=15)], render_kw={"placeholder": "Phone"})
    email = StringField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError('That username already exists. Please choose a different one.')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('That email is already registered.')

    def validate_phone(self, phone):
        if User.query.filter_by(phone=phone.data).first():
            raise ValidationError('That phone number is already registered.')

# Login Form
class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(min=5, max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')

# Routes
@app.route('/')
def home():
    return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("⚠️ Account already exists! Please log in.", "error")
            return redirect(url_for('signup')) 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # Hash password
        
        new_user = User(
            username=form.username.data,
            phone=form.phone.data,
            email=form.email.data,
            password=hashed_password  # Store the hashed password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("✅ Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):  # Check hashed password
            login_user(user)
            return redirect(url_for('dashboard'))
        flash("⚠️ Invalid email or password!", "error")
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username, email=current_user.email, phone=current_user.phone)

@app.route('/test')
@login_required
def test():
    return render_template('test.html')

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/test-instructions')
@login_required
def test_instructions():
    return render_template('test-instructions.html')

@app.route('/quiz-instructions')
@login_required
def quiz_instructions():
    return render_template('quiz-instructions.html')

# Load questions from quiz.json
with open("data/quiz.json", "r") as file:
    quiz_data = json.load(file)

@app.route('/get_quiz_questions', methods=['GET'])
def get_quiz_questions():
    return jsonify(quiz_data["questions"])

QUIZ_FILE = "quiz.json"
USER_PERFORMANCE_FILE = "user_performance.json"

def load_quiz():
    """Load quiz data from JSON."""
    try:
        with open(QUIZ_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"questions": []}

def load_user_performance():
    """Load user performance data from JSON."""
    try:
        with open(USER_PERFORMANCE_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_user_performance(data):
    """Save user performance data to JSON."""
    with open(USER_PERFORMANCE_FILE, "w") as file:
        json.dump(data, file, indent=4)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    user_id = session.get("user_id")  # Get logged-in user ID
    if not user_id:
        return jsonify({"error": "User not logged in"}), 403

    quiz_data = load_quiz()["questions"]  # Load quiz questions
    user_performance = load_user_performance()  # Load stored user answers

    # Ensure user exists in user_performance.json; if not, create an entry
    if user_id not in user_performance:
        user_performance[user_id] = {"answers": [], "score": 0}

    user_answers = request.json.get("answers", [])  # Get submitted answers from frontend
    score = 0

    # Store user's answers for this attempt
    for answer in user_answers:
        question_text = answer["question"]
        selected_answer = answer["user_answer"]
        topic = answer["topic"]

        # Find correct answer from quiz.json
        correct_answer = next(
            (q["correct_answer"] for q in quiz_data if q["question"] == question_text), None
        )

        # Calculate score
        if correct_answer:
            if selected_answer == correct_answer:
                score += 4  # Correct answer: +4 points
            elif selected_answer != "Not Answered":
                score -= 1  # Wrong answer: -1 point

        # Append user's answer to their history
        user_performance[user_id]["answers"].append({
            "question": question_text,
            "user_answer": selected_answer,
            "correct_answer": correct_answer,
            "topic": topic
        })

    # Store updated score for the user
    user_performance[user_id]["score"] = score
    save_user_performance(user_performance)

    # Determine message based on score
    if score >= 65:
        message = "confetti"
    elif score >= 40:
        message = "well_done"
    else:
        message = "check_answers"

    return jsonify({"score": score, "message": message})


@app.route('/submit')
@login_required
def submit():
    return render_template("submit.html")

@app.route('/practice_more/<topic>')
@login_required
def practice_more(topic):
    # Fetch questions from the weak topic
    question_bank = pd.read_csv("data/question_bank.csv")
    topic_questions = question_bank[question_bank["topic"] == topic].to_dict(orient="records")

    return render_template("new_questions.html", questions=topic_questions)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
