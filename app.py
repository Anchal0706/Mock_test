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

# Select number of questions
num_questions = st.number_input("How many questions?", min_value=1, max_value=20, step=1, value=5)

# Start Quiz Button
if st.button("Start Quiz") and not st.session_state.quiz_started:
    st.session_state.quiz_started = True
    st.session_state.submitted = False
    st.session_state.selected_answers = {}
    st.session_state.questions = get_random_questions(num_questions)
    st.rerun()

# Display questions if quiz started but not yet submitted
if st.session_state.quiz_started and not st.session_state.submitted:
    for i, q in enumerate(st.session_state.questions, start=1):
        if q["question"] not in st.session_state.selected_answers:
            st.session_state.selected_answers[q["question"]] = None

        st.markdown(f"<p style='font-size:18px; font-weight:bold;'>{i}. {q['question']}</p>", unsafe_allow_html=True)

        selected = st.radio("", 
            [q["option_1"], q["option_2"], q["option_3"], q["option_4"]],
            index=None,  # Allows free selection
            key=f"q{i}"
        )

        if selected:
            st.session_state.selected_answers[q["question"]] = selected

    # Submit button
    if st.button("Submit"):
        st.session_state.submitted = True
        st.rerun()

# Show Results if submitted
if st.session_state.submitted:
    st.subheader("Results:")
    correct_answers = []
    score = 0

    for i, q in enumerate(st.session_state.questions, start=1):
        user_answer = st.session_state.selected_answers[q["question"]]
        correct_answer = q[f"option_{q['correct_option']}"]

        st.markdown(f"<p style='font-size:18px; font-weight:bold;'>{i}. {q['question']}</p>", unsafe_allow_html=True)

        if user_answer == correct_answer:
            score += 1
            st.markdown(f"✅ <span style='color: green;'>{correct_answer}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"❌ <span style='color: red;'>{user_answer if user_answer else 'No Answer'}</span>", unsafe_allow_html=True)
            correct_answers.append(f"**{i}. {q['question']}** - ✅ {correct_answer}")

    # Show Score
    st.markdown(f"### Your Score: {score} / {len(st.session_state.questions)} 🎯")

    # Show all correct answers in a separate box
    if correct_answers:
        with st.expander("See All Correct Answers"):
            for ans in correct_answers:
                st.markdown(ans, unsafe_allow_html=True)

    # Restart button
    if st.button("Restart Quiz"):
        st.session_state.quiz_started = False
        st.session_state.submitted = False
        st.session_state.questions = []
        st.session_state.selected_answers = {}
        st.rerun()
