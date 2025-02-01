import json
from collections import defaultdict
import matplotlib.pyplot as plt
import os

def load_data(quiz_file, performance_file):
    with open(quiz_file, 'r') as qf, open(performance_file, 'r') as pf:
        quiz_data = json.load(qf)
        performance_data = json.load(pf)
    return quiz_data, performance_data

def calculate_scores(quiz_data, performance_data):
    topic_scores = defaultdict(lambda: defaultdict(int))  # {user_id: {topic: score}}
    topic_questions = defaultdict(int)  # {topic: total_questions}
    
    # Count total questions per topic
    for q in quiz_data['questions']:
        topic_questions[q['topic']] += 1

    # Loop through users (user_id as key)
    for user_id, responses in performance_data.items():
        user_id = str(user_id)  # Ensure user_id is treated as a string
        topic_performance = defaultdict(int)

        # Process each response
        for response in responses:
            question_id = response['question_id']
            user_answer = response['marked_answer']
            correct_answer = response['correct_answer']
            topic = response['topic']

            # Score calculation
            if user_answer == correct_answer:
                topic_performance[topic] += 4  # Correct answer = +4 points
            else:
                topic_performance[topic] -= 1  # Wrong answer = -1 point

        topic_scores[user_id] = topic_performance  # Store user scores

    return topic_scores, topic_questions

def generate_recommendations(topic_scores, topic_questions):
    recommendations = {}

    for user, scores in topic_scores.items():
        weak_topics = []
        for topic, score in scores.items():
            max_score = topic_questions[topic] * 4  # Maximum possible score per topic
            if score < 0.4 * max_score:  # If score is below 50% of max, recommend improvement
                weak_topics.append(topic)

        recs = [f"Focus on {topic} - Recommended videos, notes, and practice questions." for topic in weak_topics]
        recommendations[user] = recs if recs else ["Great job! Keep practicing."]

    return recommendations
# File paths (update as needed)
quiz_file = "data/quiz.json"
performance_file = "data/user_performance.json"

# Load and process data
quiz_data, performance_data = load_data(quiz_file, performance_file)
topic_scores, topic_questions = calculate_scores(quiz_data, performance_data)
recommendations = generate_recommendations(topic_scores, topic_questions)

def generate_pie_chart(user_id, topic_scores, recommendations, chart_dir="charts"):
    # Create directory for charts if it doesn't exist
    if not os.path.exists(chart_dir):
        os.makedirs(chart_dir)

    # Get user scores
    scores = topic_scores[user_id]
    topics = list(scores.keys())
    positive_scores = [max(0, score) for score in scores.values()]  # Positive part (correct answers)
    negative_scores = [abs(min(0, score)) for score in scores.values()]  # Negative part (wrong answers)

    # Check if scores are valid for chart generation
    if sum(positive_scores) == 0 and sum(negative_scores) == 0:  # No valid data
        print(f"User {user_id} has no scores. No chart can be generated.")
        return None

    total_scores = [pos + neg for pos, neg in zip(positive_scores, negative_scores)]
    weak_topics = []
    for topic, total_score in zip(topics, total_scores):
        max_score = topic_questions[topic] * 4  # Maximum score for this topic
        if total_score < 0.4 * max_score:  # Less than 50% of max score
            weak_topics.append(topic)
        

    # Positive = green, Negative = red
    colors = ["green" if score > 0 else "red" for topic, score in zip(topics, scores.values())]

    # Generate pie chart - including both Positive and Negative segments
    plt.figure(figsize=(8, 6))

    # Total Pie Chart
    plt.pie(
        total_scores,
        labels=topics,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
    )

    plt.title(f"Performance Analysis for User {user_id}\nWeak Topics Highlighted in Red")
    plt.legend(topics, title="Topics", loc="best")

    # Save chart to a file
    chart_path = f"{chart_dir}/user_{user_id}_analysis.png"
    plt.savefig(chart_path)
    plt.close()
    return chart_path

# Generate charts and output recommendations
for user, recs in recommendations.items():
    chart_path = generate_pie_chart(user, topic_scores, recommendations)
    print(f"User {user} Analysis Chart: {chart_path}")
    print(f"User {user} Recommendations:")
    for rec in recs:
        print(f"  - {rec}")
    print()
