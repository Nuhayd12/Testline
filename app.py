from flask import Flask, render_template, request, redirect, url_for, flash, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf import FlaskForm
import pandas as pd
import json,os,traceback

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

    # Debugging: Check if form is being validated
    if form.validate_on_submit():
        print("Form is valid")
        
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

        try:
            db.session.add(new_user)
            db.session.commit()  # Commit to save the user data
            flash("✅ Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))

        except Exception as e:
            # Debugging: Print exception for clarity
            print(f"Error: {e}")
            flash("⚠️ Something went wrong! Please try again.", "error")
            db.session.rollback()  # Rollback in case of error to maintain integrity
            return redirect(url_for('signup'))

    else:
        # Debugging: Print out form errors
        print(form.errors)

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

DATA_FOLDER = "data"
QUIZ_FILE = os.path.join(DATA_FOLDER, "quiz.json")
USER_PERFORMANCE_FILE = os.path.join(DATA_FOLDER, "user_performance.json")
DATABASE_FILE = "users.db"

if not os.path.exists(USER_PERFORMANCE_FILE) or os.path.getsize(USER_PERFORMANCE_FILE) == 0:
    with open(USER_PERFORMANCE_FILE, "w") as file:
        json.dump({}, file)

def load_quiz():
    """Load quiz data from JSON."""
    try:
        with open(QUIZ_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"questions": []}

def load_user_performance():
    """Load user performance data from JSON safely."""
    try:
        if os.path.exists(USER_PERFORMANCE_FILE) and os.path.getsize(USER_PERFORMANCE_FILE) > 0:
            with open(USER_PERFORMANCE_FILE, "r") as file:
                return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        pass
    return {} 


def save_user_performance(data):
    """Save user performance data to JSON."""
    with open(USER_PERFORMANCE_FILE, "w") as file:
        json.dump(data, file, indent=4)
        
def get_user_id():
    """Retrieve user ID from Flask-Login session."""
    if current_user.is_authenticated:
        return current_user.id
    return None

@app.route("/save_quiz", methods=["POST"])
@login_required
def save_quiz():
    """Save user's answers and generate/update user_performance.json"""
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    if not request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = request.get_json()
    user_answers = data.get("answers", {})  # Default to empty dict if missing

    if not user_answers:
        return jsonify({"error": "No answers provided"}), 400

    try:
        print(f"🔹 Received answers: {user_answers}")  # Debugging line

        # Load quiz data
        with open(QUIZ_FILE, "r") as file:
            quiz_data = json.load(file)

        # Load or create user performance data
        if os.path.exists(USER_PERFORMANCE_FILE):
            with open(USER_PERFORMANCE_FILE, "r") as file:
                user_performance = json.load(file)
        else:
            user_performance = {}

        # Ensure user performance exists for this user
        if user_id not in user_performance:
            user_performance[user_id] = []

        # Update answers instead of overwriting them
        for q in quiz_data["questions"]:
            question_id = f"q{q['id']}"
            existing_entry = next((entry for entry in user_performance[user_id] if entry["question_id"] == q["id"]), None)

            if existing_entry:
                existing_entry["marked_answer"] = user_answers.get(question_id, "Not Answered")
            else:
                user_performance[user_id].append({
                    "question_id": q["id"],
                    "question": q["question"],
                    "topic": q["topic"],
                    "marked_answer": user_answers.get(question_id, "Not Answered"),
                    "correct_answer": q["correct_answer"]
                })

        # Save updated performance data
        with open(USER_PERFORMANCE_FILE, "w") as file:
            json.dump(user_performance, file, indent=4)

        return jsonify({"message": "Answers saved successfully!", "saved": True})

    except Exception as e:
        print("🔥 Error occurred while saving quiz answers!")  # Debugging
        traceback.print_exc()  # Print full error traceback in the terminal
        return jsonify({"error": str(e)}), 500


@app.route("/submit_quiz", methods=["POST"])
@login_required
def submit_quiz():
    """Calculate quiz score and return results."""
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "User not authenticated"}), 401

    if not os.path.exists(USER_PERFORMANCE_FILE):
        return jsonify({"error": "User performance data not found!"}), 500

    with open(USER_PERFORMANCE_FILE, "r") as file:
        user_performance = json.load(file)

    if user_id not in user_performance:
        return jsonify({"error": "No answers recorded for this user!"}), 500

    score = sum(4 for entry in user_performance[user_id] if entry["marked_answer"] == entry["correct_answer"])
    total_questions = len(user_performance[user_id])

    return jsonify({
        "message": "Quiz submitted successfully!",
        "score": f"{score}/{total_questions}",
        "answers": user_performance[user_id]
    })



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
