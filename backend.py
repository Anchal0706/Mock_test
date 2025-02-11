import pandas as pd
import random

def load_questions(filename="questions.csv"):
    """Load questions from CSV and return as a list of dictionaries."""
    df = pd.read_csv(filename)
    return df.to_dict(orient="records")

def get_random_questions(num_questions):
    """Fetch a random subset of questions."""
    questions = load_questions()
    random.shuffle(questions)
    return questions[:num_questions]
