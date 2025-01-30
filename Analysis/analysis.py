import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


with open('quiz_data.json') as f:
    quiz_data = json.load(f)

with open('submission_data.json') as f:
    submission_data = json.load(f)

with open('history_data.json') as f:
    history_data = json.load(f)

# Extracting detals related tot the quiz
quiz_id = quiz_data['quiz']['id']
quiz_topic = quiz_data['quiz']['topic']
questions = quiz_data['quiz']['questions']

# Dataframe for each question
questions_df = pd.DataFrame(questions)


def is_correct(qid):
    for question in quiz_data['quiz']['questions']:
        if question['id'] == qid:
            return any(opt['is_correct'] for opt in question['options'])
    return False

questions_df['is_correct'] = questions_df['id'].map(is_correct)

# Getting the user performance badsed on user history of answering the quizes
history_df = pd.DataFrame(history_data)
history_df['accuracy'] = history_df['accuracy'].str.replace('%', '').astype(float)
history_df['correct_answers'] = history_df['correct_answers'].astype(int)
history_df['incorrect_answers'] = history_df['incorrect_answers'].astype(int)

# Performance
performance_trend = history_df[['submitted_at', 'accuracy']]
performance_trend.loc[:,'submitted_at'] = pd.to_datetime(performance_trend['submitted_at'])
performance_trend = performance_trend.sort_values('submitted_at')

# Let's plot the graph for accuracy Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(data=performance_trend, x='submitted_at', y='accuracy', marker='o')
plt.title('User Performance Over Time')
plt.xlabel('Date')
plt.ylabel('Accuracy (%)')
plt.xticks(rotation=45)
plt.grid()
plt.show()


# Insights for teh mentors
print("User Performance Summary")
print(f"Overall Accuracy: {history_df['accuracy'].iloc[0]}%")
