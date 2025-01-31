import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class QuizPerformanceAnalyzer:
    def __init__(self, user_id: str):
        """
        Initialize the performance analyzer for a specific user
        
        Args:
            user_id (str): Unique identifier for the student
        """
        self.user_id = user_id
        self.quiz_history = pd.DataFrame(columns=[
            'date', 'topic', 'total_questions', 
            'correct_answers', 'incorrect_answers', 
            'score_percentage'
        ])
    
    def add_quiz_result(self, date: str, topic: str, 
                         total_questions: int, 
                         correct_answers: int) -> None:
        """
        Add a new quiz result to the user's history
        
        Args:
            date (str): Date of the quiz
            topic (str): Subject or topic of the quiz
            total_questions (int): Total number of questions
            correct_answers (int): Number of correctly answered questions
        """
        incorrect_answers = total_questions - correct_answers
        score_percentage = (correct_answers / total_questions) * 100
        
        new_entry = pd.DataFrame({
            'date': [date],
            'topic': [topic],
            'total_questions': [total_questions],
            'correct_answers': [correct_answers],
            'incorrect_answers': [incorrect_answers],
            'score_percentage': [score_percentage]
        })
        
        self.quiz_history = pd.concat([self.quiz_history, new_entry], ignore_index=True)
    
    def analyze_performance(self) -> Dict[str, float]:
        """
        Analyze overall performance across different topics
        
        Returns:
            Dict containing performance metrics for each topic
        """
        topic_performance = self.quiz_history.groupby('topic').agg({
            'score_percentage': ['mean', 'count'],
            'incorrect_answers': 'sum'
        })
        
        performance_dict = {}
        for topic, stats in topic_performance.iterrows():
            performance_dict[topic] = {
                'average_score': round(stats[('score_percentage', 'mean')], 2),
                'total_quizzes': stats[('score_percentage', 'count')],
                'total_incorrect': stats[('incorrect_answers', 'sum')]
            }
        
        return performance_dict
    
    def identify_weak_topics(self, threshold: float = 60.0) -> List[str]:
        """
        Identify topics where performance is below a specified threshold
        
        Args:
            threshold (float): Performance threshold percentage
        
        Returns:
            List of weak topics
        """
        performance = self.analyze_performance()
        weak_topics = [
            topic for topic, metrics in performance.items() 
            if metrics['average_score'] < threshold
        ]
        
        return weak_topics
    
    def generate_recommendations(self) -> Dict[str, str]:
        """
        Generate personalized learning recommendations
        
        Returns:
            Dictionary of recommendations for improvement
        """
        weak_topics = self.identify_weak_topics()
        recommendations = {}
        
        difficulty_map = {
            'low': ['Review fundamental concepts', 'Practice basic problems'],
            'medium': ['Watch explanatory videos', 'Solve intermediate problems'],
            'high': ['Solve complex problem sets', 'Analyze advanced case studies']
        }
        
        for topic in weak_topics:
            # Determine difficulty based on performance
            performance = self.analyze_performance()[topic]
            
            if performance['average_score'] < 40:
                difficulty = 'low'
            elif 40 <= performance['average_score'] < 60:
                difficulty = 'medium'
            else:
                difficulty = 'high'
            
            recommendations[topic] = {
                'recommendation': np.random.choice(difficulty_map[difficulty]),
                'current_score': performance['average_score']
            }
        
        return recommendations

def main():
    # Example usage
    analyzer = QuizPerformanceAnalyzer('student_123')
    
    # Simulating quiz results
    analyzer.add_quiz_result('2024-01-15', 'Mathematics', 20, 12)
    analyzer.add_quiz_result('2024-01-22', 'Science', 25, 15)
    analyzer.add_quiz_result('2024-01-29', 'Mathematics', 30, 18)
    
    # Analyze performance
    performance = analyzer.analyze_performance()
    print("Performance Analysis:")
    for topic, metrics in performance.items():
        print(f"{topic}: {metrics}")
    
    # Generate recommendations
    recommendations = analyzer.generate_recommendations()
    print("\nPersonalized Recommendations:")
    for topic, details in recommendations.items():
        print(f"{topic}: {details['recommendation']} (Current Score: {details['current_score']}%)")

if __name__ == "__main__":
    main()