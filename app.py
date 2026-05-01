import streamlit as st
import matplotlib.pyplot as plt
from analyzer import (
    extract_text,
    extract_skills,
    calculate_score,
    match_score,
    generate_feedback,
    match_with_job_description
)
from database import save_result
from report import generate_pdf

st.set_page_config(page_title="AI Career System", layout="wide")

# 🌈 Custom styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    h1 {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🚀 AI Career Intelligence System")
st.markdown("### Improve your resume with AI-powered insights")

# Layout columns
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("📄 Upload Resume (PDF)")

with col2:
    job_desc = st.text_area("🧾 Paste Job Description")

if file:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text(file)
    skills = extract_skills(text)
    score = calculate_score(skills)
    match, missing = match_score(skills)

    st.markdown("---")

    # 🔹 Metrics Row
    col1, col2, col3 = st.columns(3)

    col1.metric("📈 ATS Score", f"{score}%")
    col2.metric("🎯 Job Match", f"{match}%")
    col3.metric("🧠 Skills Found", len(skills))

    st.markdown("---")

    # 🔹 Skills
    st.subheader("🧠 Extracted Skills")
    st.write(", ".join(skills))

    # 🔹 Chart
    st.subheader("📊 Skills Overview")

    fig, ax = plt.subplots()
    ax.bar(["Matched", "Missing"], [len(skills), len(missing)])
    st.pyplot(fig)

    # 🔹 Missing
    st.subheader("❌ Missing Skills")
    st.write(", ".join(missing))

    # 🔹 AI Suggestions
    st.subheader("🤖 AI Suggestions")
    feedback = generate_feedback(skills, missing)
    st.info(feedback)

    # 🔹 JD Matching
    if job_desc:
        jd_score, jd_missing = match_with_job_description(text, job_desc)

        st.markdown("---")
        st.subheader("📄 Job Description Match")

        st.metric("🎯 JD Match Score", f"{jd_score}%")
        st.write("Missing from JD:", ", ".join(jd_missing))

    # Save to DB
    save_result("User", score, skills)

    # 📄 PDF
    data = {
        "skills": skills,
        "score": score,
        "missing": missing,
        "feedback": feedback
    }

    pdf_file = generate_pdf(data)

    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Report",
            data=f,
            file_name="resume_report.pdf",
            mime="application/pdf"
        )

    st.success("🎉 Analysis Complete!")