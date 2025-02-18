import pandas as pd
import random

def load_questions(filename="questions.csv"):
    """Load questions from CSV and return as a DataFrame."""
    try:
        df = pd.read_csv(filename)
        return df
    except FileNotFoundError:
        print("Error: questions.csv file not found!")
        return pd.DataFrame()  # Return an empty DataFrame if file not found

def get_filtered_questions(category, difficulty="Any", num_questions=10):
    """
    Fetch a subset of questions filtered by category and difficulty.
    
    Parameters:
    - category (str): The category of questions to filter by (e.g., "Python", "Data Science").
    - difficulty (str): The difficulty level to filter by. Options: "Any", "Easy", "Medium", "Hard".
    - num_questions (int): The number of questions to return.
    
    Returns:
    - List of dictionaries, where each dictionary represents a question.
    """
    questions_df = load_questions()
    
    if questions_df.empty:
        return []
    
    # Filter by category if not "All Python questions"
    if category != "All Python questions":
        questions_df = questions_df[questions_df["category"] == category]
    
    # Filter by difficulty if not "Any"
    if difficulty != "Any":
        questions_df = questions_df[questions_df["difficulty"] == difficulty]
    
    # Shuffle and return the requested number of questions
    questions = questions_df.to_dict(orient="records")
    random.shuffle(questions)
    return questions[:num_questions]