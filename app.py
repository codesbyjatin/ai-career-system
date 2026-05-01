import streamlit as st
from analyzer import extract_text, extract_skills, calculate_score, match_score
from database import save_result

st.title("AI Career Intelligence System")

file = st.file_uploader("Upload Resume (PDF)")

if file:
    text = extract_text(file)
    skills = extract_skills(text)
    score = calculate_score(skills)

    match, missing = match_score(skills)

    st.subheader("Results")
    st.write("Skills:", skills)
    st.write("ATS Score:", score)
    st.write("Job Match:", match)
    st.write("Missing Skills:", missing)

    save_result("User", score, skills)