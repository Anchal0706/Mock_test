import pandas as pd
import random


def load_questions(filename="questions.csv"):
    """Load questions from CSV and return as a list of dictionaries."""
    df = pd.read_csv(filename)
    return df.to_dict(orient="records")


def get_random_questions(num_questions, category=None):
    """Fetch a random subset of questions, optionally filtered by category."""
    questions = load_questions()


    if category:
        if category == "All Python questions":
            # Select unique questions across all categories
            random.shuffle(questions)
        else:
            questions = [q for q in questions if q["category"] == category]


    random.shuffle(questions)
    return questions[:num_questions]
