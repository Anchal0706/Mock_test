import streamlit as st
import pandas as pd
import os
import random


# Set page title and layout
st.set_page_config(page_title="Python Mock Test", layout="wide")


# Load questions from CSV file
@st.cache_data
def load_questions():
    file_path = "questions.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
       
        # Ensure 'difficulty' column exists, else add it with default value
        if "difficulty" not in df.columns:
            df["difficulty"] = "Any"
       
        return df
    else:
        st.error("⚠️ Error: 'questions.csv' not found!")
        return pd.DataFrame()  # Return an empty DataFrame if file not found


questions_df = load_questions()


# Ensure the questions are loaded
if questions_df is None or questions_df.empty:
    st.error("⚠️ No questions available. Please check 'questions.csv'!")
    st.stop()


# Categories
categories = questions_df["category"].unique()


def reset_questions():
    """Filter questions based on selected category and difficulty."""
    filtered_questions = questions_df[
        (questions_df["category"] == st.session_state.selected_category) &
        ((questions_df["difficulty"] == st.session_state.difficulty) | (st.session_state.difficulty == "Any"))
    ]
   
    num_available = len(filtered_questions)
    num_to_sample = min(num_available, st.session_state.num_questions)
   
    st.session_state.questions = filtered_questions.sample(n=num_to_sample, replace=False).to_dict(orient="records")
    st.session_state.answers = {}
    st.session_state.current_question_index = 0  # Track the current question index
   
    if num_to_sample < st.session_state.num_questions:
        st.warning(f"⚠️ Only {num_available} questions available for this selection.")


# Custom CSS for styling
st.markdown("""
    <style>
        .header {
            display: flex;
            justify-content: space-around;
            background-color: #2E3B4E;
            padding: 10px;
            border-radius: 10px;
        }
        .header a {
            color: white;
            text-decoration: none;
            font-size: 20px;
        }
        .box {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .back-button {
            margin-top: 20px;
        }
        .question-text {
            font-size: 24px !important;
            margin-bottom: 20px;
        }
        .category-text {
            font-size: 28px !important;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .quiz-title {
            font-size: 26px !important;
            margin-bottom: 20px;
        }
        .about-box {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
        }
        .project-box {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .contact-box {
            border: 2px solid #4CAF50;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
        }
    </style>
    <div class="header">
        <a href="#" onclick="window.location.href='/'">Home</a>
        <a href="#" onclick="window.location.href='/?page=about'">About Product</a>
        <a href="#" onclick="window.location.href='/?page=explore'">Explore More</a>
        <a href="#" onclick="window.location.href='/?page=contact'">Contact Us</a>
    </div>
""", unsafe_allow_html=True)


# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"


# Function to handle page navigation
def navigate_to_page(page):
    st.session_state.page = page
    st.rerun()


# ✅ Home Page
if st.session_state.page == "home":
    st.title("Welcome to AI Agents-Based MCQs")
    st.image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg", width=200)
    st.write("Test your skills here.")
   
    if st.button("➡️ Next"):
        st.session_state.page = "category_selection"
        st.rerun()


# ✅ Category Selection Page
elif st.session_state.page == "category_selection":
    st.title("📌 Choose Your Quiz Settings")
   
    topic = st.text_input("Enter topic:")
    num_questions = st.number_input("Enter # of questions you want:", min_value=1, step=1, value=5)
    difficulty = st.selectbox("Select difficulty level:", ["Any", "Easy", "Medium", "Hard"])
    category = st.selectbox("Choose a category", ["Select"] + list(categories), index=0)
   
    if category != "Select":
        st.session_state.selected_category = category
        st.session_state.difficulty = difficulty
        st.session_state.num_questions = num_questions
        reset_questions()
        st.session_state.page = "quiz"
        st.rerun()
   
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ✅ Quiz Page (Sequential Question Format)
elif st.session_state.page == "quiz":
    st.markdown(f'<div class="category-text">📚 {st.session_state.selected_category} Quiz</div>', unsafe_allow_html=True)
   
    # Dynamic title with topic, number of questions, and difficulty level
    st.markdown(f'<div class="quiz-title">Here is your <strong>{st.session_state.selected_category}</strong> quiz consisting <strong>{st.session_state.num_questions} questions</strong> of <strong>{st.session_state.difficulty}</strong> level.</div>', unsafe_allow_html=True)
   
    question = st.session_state.questions[st.session_state.current_question_index]
    st.markdown(f'<div class="question-text">{st.session_state.current_question_index + 1}. {question["question"]}</div>', unsafe_allow_html=True)
   
    options = [question["option_1"], question["option_2"], question["option_3"], question["option_4"]]
    selected_option = st.radio("", options, key=f"q_{st.session_state.current_question_index}", index=None)
   
    if st.button("Submit and Move to Next"):
        if selected_option:
            st.session_state.answers[question["question"]] = selected_option
           
            if st.session_state.current_question_index + 1 < len(st.session_state.questions):
                st.session_state.current_question_index += 1
                st.rerun()
            else:
                st.session_state.page = "results"
                st.rerun()
   
    # Back button at the bottom of the quiz page
    if st.button("⬅️ Back to Category Selection", key="back_quiz"):
        st.session_state.page = "category_selection"
        st.rerun()


# ✅ Results Page
elif st.session_state.page == "results":
    st.title("📊 Quiz Results")
    correct_count = sum(1 for q in st.session_state.questions if st.session_state.answers.get(q["question"]) == q[f"option_{q['correct_option']}"])
    total_questions = len(st.session_state.questions)
   
    st.markdown(f'<div class="box">Your Score: {correct_count} out of {total_questions}</div>', unsafe_allow_html=True)
   
    if st.button("🔄 Play Again"):
        st.session_state.page = "category_selection"
        st.session_state.answers = {}
        st.rerun()
   
    # Back button at the bottom of the results page
    if st.button("⬅️ Back to Category Selection", key="back_results"):
        st.session_state.page = "category_selection"
        st.rerun()


# ✅ About Product Page
elif st.session_state.page == "about":
    st.title("About Product")
   
    # Two parallel boxes
    col1, col2 = st.columns(2)
   
    with col1:
        st.markdown('<div class="about-box">Flow of the Project</div>', unsafe_allow_html=True)
   
    with col2:
        st.markdown('<div class="about-box"><img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" width="100"><br><video controls><source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4"></video></div>', unsafe_allow_html=True)
   
    # Back button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ✅ Explore More Page
elif st.session_state.page == "explore":
    st.title("Explore More")
   
    # List of projects with "View More" buttons
    for i in range(1, 6):
        st.markdown(f'<div class="project-box">Project {i}<button style="float: right;">View More</button></div>', unsafe_allow_html=True)
   
    # Back button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()


# ✅ Contact Us Page
elif st.session_state.page == "contact":
    st.title("Contact Us")
   
    # Contact details
    st.markdown("""
        <div class="contact-box">
            <p>Contact Number: +1234567890</p>
            <p>Email: example@example.com</p>
            <p>Address: 123 Street, City, Country</p>
            <p>LinkedIn: <a href="https://www.linkedin.com">LinkedIn Profile</a></p>
        </div>
    """, unsafe_allow_html=True)
   
    # Back button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()