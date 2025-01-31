import pandas as pd

# Load existing data
quiz_metadata = pd.read_csv("data/quiz_metadata.csv")
question_bank = pd.read_csv("data/question_bank.csv")
user_performance = pd.read_csv("data/user_performance.csv")

# Identify weak topics per user
user_analysis = user_performance.merge(question_bank, left_on="Question_ID", right_on="question_id")

# Calculate accuracy per topic
topic_performance = user_analysis.groupby(["User_ID", "topic"])["Is_Correct"].mean().reset_index()

# Define a threshold for weak topics
weak_threshold = 0.6  # If accuracy < 60%, it's a weak topic

# Get weak topics
weak_topics = topic_performance[topic_performance["Is_Correct"] < weak_threshold]

# Generate recommendations
recommendations = []
for index, row in weak_topics.iterrows():
    topic = row["topic"]
    user_id = row["User_ID"]
    
    # Define improvement strategies
    suggestion = f"Review {topic} concepts, reattempt quiz, focus on explanation videos"
    
    recommendations.append({"User_ID": user_id, "Weak_Topics": topic, "Suggested_Actions": suggestion})

# Convert to DataFrame
ai_recommendations = pd.DataFrame(recommendations)

# Save recommendations
ai_recommendations.to_csv("data/ai_recommendations.csv", index=False)

# Return updated recommendations
print(ai_recommendations)
