import streamlit as st
from backend import get_random_questions

st.title("Python Mock Test")

# Initialize session state
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "selected_answers" not in st.session_state:
    st.session_state.selected_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "questions" not in st.session_state:
    st.session_state.questions = []

# Centered start button
if not st.session_state.quiz_started:
    if st.button("Start Python Mock Test"):
        st.session_state.quiz_started = True
        st.session_state.submitted = False
        st.session_state.selected_answers = {}
        st.session_state.questions = get_random_questions(5)  # Defaulting to 5 questions
        st.rerun()

# Display questions if quiz started
if st.session_state.quiz_started:
    for i, q in enumerate(st.session_state.questions, start=1):
        if q["question"] not in st.session_state.selected_answers:
            st.session_state.selected_answers[q["question"]] = None
        
        selected = st.radio(f"{i}. {q['question']}", 
            [q["option_1"], q["option_2"], q["option_3"], q["option_4"]],
            index=None, key=f"q{i}")
        
        correct_answer = q[f"option_{q['correct_option']}"]
        
        if selected:
            st.session_state.selected_answers[q["question"]] = selected
            if selected == correct_answer:
                st.markdown(f"✅ <span style='color: green;'>Correct</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"❌ <span style='color: red;'>Incorrect</span>", unsafe_allow_html=True)
    
    # Submit button
    if st.button("Submit"):
        st.session_state.submitted = True
        st.session_state.quiz_started = False  # Reset quiz state for new questions
        st.session_state.questions = get_random_questions(5)  # Fetch new questions
        st.rerun()
