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

# Select number of questions
num_questions = st.number_input("How many questions?", min_value=1, max_value=20, step=1, value=5)

# Start Quiz Button
if st.button("Start Quiz"):
    st.session_state.quiz_started = True
    st.session_state.selected_answers = {}
    st.session_state.submitted = False
    st.session_state.questions = get_random_questions(num_questions)
    st.rerun()

# Display questions if quiz started
if st.session_state.quiz_started:
    for i, q in enumerate(st.session_state.questions):
        selected = st.radio(q["question"], 
            [q["option_1"], q["option_2"], q["option_3"], q["option_4"]],
            key=f"q{i}"
        )
        st.session_state.selected_answers[q["question"]] = selected

    # Submit button
    if st.button("Submit"):
        st.session_state.submitted = True
        st.rerun()

# Show Results if submitted
if st.session_state.submitted:
    st.subheader("Results:")
    correct_answers = []

    for i, q in enumerate(st.session_state.questions):
        user_answer = st.session_state.selected_answers[q["question"]]
        correct_answer = q[f"option_{q['correct_option']}"]

        # Show correct & incorrect answers with colors
        if user_answer == correct_answer:
            st.markdown(f"✅ **{q['question']}** - <span style='color: green;'>{correct_answer}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"❌ **{q['question']}** - <span style='color: red;'>{user_answer}</span>", unsafe_allow_html=True)
            correct_answers.append(f"**{q['question']}** - ✅ {correct_answer}")

    # Show all correct answers in a separate box
    if correct_answers:
        with st.expander("See All Correct Answers"):
            for ans in correct_answers:
                st.markdown(ans, unsafe_allow_html=True)

    # Restart button
    if st.button("Restart Quiz"):
        st.session_state.quiz_started = False
        st.session_state.submitted = False
        st.rerun()
