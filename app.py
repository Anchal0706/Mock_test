import streamlit as st
from backend import get_random_questions

st.title("Python Mock Test")

# Redirect to category page
def category_page(category_name):
    st.session_state.category_selected = category_name
    st.session_state.page = "category_page"
    st.rerun()

# Handle navigation
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category_selected" not in st.session_state:
    st.session_state.category_selected = ""

if st.session_state.page == "home":
    categories = ["List", "Set", "String", "Loops"]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("List"):
            category_page("List")
    with col2:
        if st.button("Set"):
            category_page("Set")
    with col3:
        if st.button("String"):
            category_page("String")
    with col4:
        if st.button("Loops"):
            category_page("Loops")
    
    # Centered start button
    if st.button("Basic Python"):
        st.session_state.page = "quiz"
        st.session_state.quiz_started = True
        st.session_state.submitted = False
        st.session_state.selected_answers = {}
        st.session_state.questions = get_random_questions(5)  # Defaulting to 5 questions
        st.session_state.page_number = 1  # Reset page number
        st.rerun()

elif st.session_state.page == "category_page":
    st.markdown(f"<h2 style='text-align: center;'>Questions loading; Please wait</h2>", unsafe_allow_html=True)
    
    # Back button to home page
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()

elif st.session_state.page == "quiz":
    st.subheader(f"Page {st.session_state.page_number}")
    
    for i, q in enumerate(st.session_state.questions, start=1):
        if q["question"] not in st.session_state.selected_answers:
            st.session_state.selected_answers[q["question"]] = None
        
        st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{i}. {q['question']}</p>", unsafe_allow_html=True)
        
        selected = st.radio("", 
            [q["option_1"], q["option_2"], q["option_3"], q["option_4"]],
            index=None, key=f"q{i}")
        
        correct_answer = q[f"option_{q['correct_option']}"]
        
        if selected:
            st.session_state.selected_answers[q["question"]] = selected
            if selected == correct_answer:
                st.markdown("✅ <span style='color: green;'>Correct</span>", unsafe_allow_html=True)
            else:
                st.markdown("❌ <span style='color: red;'>Incorrect</span>", unsafe_allow_html=True)
    
    # Submit button
    if st.button("Next Page"):
        st.session_state.submitted = True
        st.session_state.page_number += 1  # Increment page number
        st.session_state.questions = get_random_questions(5)  # Fetch new questions
        st.session_state.selected_answers = {}  # Reset answers
        st.rerun()
    
    # Back button to home page
    if st.button("Back"):
        st.session_state.page = "home"
        st.rerun()
