import pandas as pd

# Creating Quiz Metadata CSV
quiz_metadata = pd.DataFrame([
    {"Quiz_ID": 51, "Subject": "Biology", "Topic": "Minor Test", "Difficulty": "Medium", "Total_Questions": 45, "Duration (min)": 45},
    {"Quiz_ID": 52, "Subject": "Physics", "Topic": "Kinematics", "Difficulty": "Hard", "Total_Questions": 30, "Duration (min)": 30},
    {"Quiz_ID": 53, "Subject": "Chemistry", "Topic": "Organic Chemistry", "Difficulty": "Medium", "Total_Questions": 40, "Duration (min)": 40}
])
quiz_metadata.to_csv("/mnt/data/quiz_metadata.csv", index=False)

question_bank = pd.DataFrame([
    {"quiz_id": 51, "question_id": 1001, "question": "What is the powerhouse of the cell?",
     "option_1": "Mitochondria", "option_2": "Ribosome", "option_3": "Nucleus", "option_4": "Golgi Apparatus",
     "correct_option": "option_1", "difficulty": "Easy", "topic": "Cell Biology"},
    
    {"quiz_id": 51, "question_id": 1002, "question": "What is the main function of the large intestine?",
     "option_1": "Digestion", "option_2": "Absorption of nutrients", "option_3": "Water absorption", "option_4": "Protein synthesis",
     "correct_option": "option_3", "difficulty": "Medium", "topic": "Human Physiology"},
    
    {"quiz_id": 51, "question_id": 1003, "question": "Which of the following is a prokaryotic organism?",
     "option_1": "Fungi", "option_2": "Bacteria", "option_3": "Algae", "option_4": "Protozoa",
     "correct_option": "option_2", "difficulty": "Easy", "topic": "Microbiology"},
    
    {"quiz_id": 51, "question_id": 1004, "question": "What is the role of hemoglobin in the blood?",
     "option_1": "Transport oxygen", "option_2": "Clot blood", "option_3": "Fight infections", "option_4": "Regulate pH",
     "correct_option": "option_1", "difficulty": "Medium", "topic": "Human Physiology"},
    
    {"quiz_id": 51, "question_id": 1005, "question": "Which macromolecule serves as the primary source of energy?",
     "option_1": "Proteins", "option_2": "Lipids", "option_3": "Carbohydrates", "option_4": "Nucleic acids",
     "correct_option": "option_3", "difficulty": "Easy", "topic": "Biochemistry"}
])

question_bank.to_csv("/mnt/data/question_bank.csv", index=False)

# Creating User Performance CSV
user_performance = pd.DataFrame([
    {"Attempt_ID": 2001, "User_ID": 1, "Quiz_ID": 51, "Question_ID": 1001, "Is_Correct": 1, "Time_Taken (sec)": 30},
    {"Attempt_ID": 2002, "User_ID": 1, "Quiz_ID": 51, "Question_ID": 1002, "Is_Correct": 0, "Time_Taken (sec)": 45},
    {"Attempt_ID": 2003, "User_ID": 1, "Quiz_ID": 52, "Question_ID": 1003, "Is_Correct": 1, "Time_Taken (sec)": 25}
])
user_performance.to_csv("/mnt/data/user_performance.csv", index=False)

# Creating AI Recommendations CSV
ai_recommendations = pd.DataFrame([
    {"User_ID": 1, "Weak_Topics": "Body Fluids & Circulation", "Suggested_Actions": "Revise circulation concepts, focus on diagrams"},
    {"User_ID": 1, "Weak_Topics": "Kinematics", "Suggested_Actions": "Practice motion equations, attempt more hard-level questions"}
])
ai_recommendations.to_csv("/mnt/data/ai_recommendations.csv", index=False)

# Return file paths
["data/quiz_metadata.csv", "data/question_bank.csv", "data/user_performance.csv", "data/ai_recommendations.csv"]
