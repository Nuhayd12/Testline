# Student Analytics & Recommendation System

## Overview
A comprehensive web-based platform that enables students to take subject-specific quizzes (currently focused on Biology), analyze their performance through detailed visualizations, and receive personalized topic recommendations based on their learning patterns. The system employs machine learning to provide targeted learning suggestions and interactive performance analytics.

## Features
- **User Authentication**: Secure login/signup system with password hashing
- **Interactive Quizzes**: Topic-based assessment system
- **Performance Analytics**: 
  - Visual representation of student performance
  - Accuracy tracking across multiple attempts
  - Temporal analysis of improvement
- **AI-Powered Recommendations**: 
  - Personalized topic suggestions
  - Custom learning path generation
  - Video resource recommendations

## Project Structure
```
├── _pycache_
├── Analysis/
│   ├── JSON data/
│   ├── analysis.py
│   └── charts/
│       ├── user_1_analysis.png
│       ├── user_2_analysis.png
│       └── ...
├── data/
│   ├── quiz.json
│   └── user_performance.json
├── Demo-Model/
├── static/
│   └── styles.css
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   ├── quiz-instructions.html
│   ├── quiz.html
│   ├── signup.html
│   ├── submit.html
│   ├── test-instructions.html
│   └── test.html
├── app.py
├── recommendation.py
├── users.db
└── vercer.json
```

## Technical Requirements
### Prerequisites
- Python 3.7+
- Flask web framework
- SQLite3

### Key Dependencies
```
Flask==2.0.1
matplotlib==3.4.3
numpy==1.21.2
pandas==1.3.3
scikit-learn==0.24.2
sqlite3
```

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## Usage
1. **User Registration/Login**
   - Navigate to `/signup` to create a new account
   - Use `/login` for existing users

2. **Taking Quizzes**
   - Access available quizzes from the dashboard
   - Follow quiz instructions
   - Submit answers for immediate feedback

3. **Viewing Analytics**
   - Navigate to the analysis section after quiz completion
   - View performance charts and statistics
   - Access personalized recommendations

4. **Recommendations**
   - System automatically generates topic suggestions
   - Access recommended video resources
   - Track progress on suggested topics

## System Components

### analysis.py
Handles data processing and visualization:
- Processes JSON quiz data
- Generates performance charts
- Calculates accuracy metrics

### recommendation.py
Implements the recommendation system:
- AI model for personalized suggestions
- Performance pattern analysis
- Learning resource matching

### app.py
Main application file:
- Route handling
- Business logic implementation
- User session management

### users.db
SQLite database for:
- User authentication
- Profile management
- Performance tracking

## Security Features
- Password hashing for user security
- Session management
- Protected routes
- Input validation

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License
[MIT License](LICENSE)

## Support
For support or queries, please contact [Your Contact Information]

## Future Enhancements
- Additional subject areas
- Advanced analytics features
- Mobile application
- Real-time progress tracking
- Peer comparison features
- Integration with external learning resources


## LOGIN CREDENTIALS FOR TESTING THE APPLICATION

- username: test_student
- phone: 10-digit number random
- email test_student@gmail.com
- password - tests123 (Will be hashed!)