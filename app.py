import streamlit as st
from backend import get_random_questions


st.set_page_config(page_title="Python Mock Test", page_icon="🐍")


st.markdown("""
    <style>
        .center-text {
            text-align: center;
        }
        .center-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .correct {
            color: green;
            font-weight: bold;
        }
        .incorrect {
            color: red;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize session state variables
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category_selected" not in st.session_state:
    st.session_state.category_selected = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "questions" not in st.session_state:
    st.session_state.questions = []


def load_new_questions():
    """Fetch new random questions for the selected category."""
    st.session_state.questions = get_random_questions(5, st.session_state.category_selected)
    st.session_state.selected_answers = {}
    st.session_state.submitted = False


if st.session_state.page == "home":
    st.markdown("<h1 class='center-text'>Python Mock Test</h1>", unsafe_allow_html=True)
    st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg' width='300' class='center-image'>", unsafe_allow_html=True)


    if st.button("Start Test"):
        st.session_state.page = "category"
        st.rerun()


elif st.session_state.page == "category":
    st.markdown("<h2 class='center-text'>Select the Category</h2>", unsafe_allow_html=True)


    categories = ["List", "Set", "String", "Loops", "All Python questions"]
    category = st.selectbox("Choose a category", ["Select a category"] + categories)


    if st.button("Start Quiz") and category != "Select a category":
        st.session_state.category_selected = category
        st.session_state.page = "quiz"
        st.session_state.quiz_started = True
        load_new_questions()
        st.rerun()


    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()


elif st.session_state.page == "quiz":
    st.subheader(f"Category: {st.session_state.category_selected}")


    for i, question_data in enumerate(st.session_state.questions, start=1):
        question_text = question_data["question"]
        correct_answer = question_data[f"option_{question_data['correct_option']}"]


        st.markdown(f"<p style='font-size:20px; font-weight:bold;'>Q{i}: {question_text}</p>", unsafe_allow_html=True)


        selected_answer = st.radio("",
            [question_data["option_1"], question_data["option_2"], question_data["option_3"], question_data["option_4"]],
            index=None, key=f"q{i}")


        if selected_answer:
            st.session_state.selected_answers[question_text] = selected_answer
            if selected_answer == correct_answer:
                st.markdown("<p class='correct'>✅ Correct!</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p class='incorrect'>❌ Incorrect! The correct answer is: {correct_answer}</p>", unsafe_allow_html=True)


    if st.button("Submit Quiz"):
        st.session_state.submitted = True
        st.rerun()


    if st.session_state.submitted:
        correct_count = sum(1 for q in st.session_state.questions
                            if st.session_state.selected_answers.get(q["question"]) == q[f"option_{q['correct_option']}"])
       
        st.markdown(f"<h3>You got {correct_count} out of {len(st.session_state.questions)} correct!</h3>", unsafe_allow_html=True)


        if correct_count == len(st.session_state.questions):
            st.markdown("<h3 style='color: green;'>Well done, keep it up! 🎉</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: red;'>Try again and don't do the same mistake! ❌</h3>", unsafe_allow_html=True)
       
        if st.button("Try Again"):
            load_new_questions()
            st.rerun()


    if st.button("Back to Categories"):
        st.session_state.page = "category"
        st.rerun()