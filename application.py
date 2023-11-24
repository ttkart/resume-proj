import streamlit as st
from Resume_scanner import compare

# Initialize session state
if 'saved_job_descriptions' not in st.session_state:
    st.session_state.saved_job_descriptions = {}
if 'uploaded_resumes' not in st.session_state:
    st.session_state.uploaded_resumes = {}

# Title and description
st.title("Resume Ranker")
st.write("Upload multiple resumes and provide job descriptions to rank resumes by similarity.")

# Upload multiple resumes with names
st.header("Upload Resumes")
uploaded_files = st.file_uploader("Upload resumes (PDF format)", type=["pdf"], accept_multiple_files=True)
uploaded_resume_names = [st.text_input(f"Name for Resume {i + 1}") for i in range(len(uploaded_files))]

# Save job descriptions with names
st.header("Save Job Descriptions")
new_job_description_name = st.text_input("Enter a name for the job description")
new_job_description_text = st.text_area("Enter a job description", height=200)
if st.button("Save Job Description") and new_job_description_name:
    st.session_state.saved_job_descriptions[new_job_description_name] = new_job_description_text
    new_job_description_name = ""
    new_job_description_text = ""
    st.rerun()

# Select a saved job description
st.header("Select a Job Description")
selected_job_description = st.selectbox("Select a Job Description", list(st.session_state.saved_job_descriptions.keys()))

# Button to calculate similarity scores for each named resume
if selected_job_description and uploaded_files:
    if st.button("Calculate Similarity"):
        job_description_text = st.session_state.saved_job_descriptions[selected_job_description]
        scores = compare(uploaded_files, job_description_text)
        
        st.header(f"Job Description: {selected_job_description}")

        # Create a list of tuples with resume names and their similarity scores
        resume_scores = list(zip(uploaded_resume_names, scores))
        # Sort the list by similarity scores in descending order
        sorted_resume_scores = sorted(resume_scores, key=lambda x: x[1], reverse=True)
        for i, (resume_name, score) in enumerate(sorted_resume_scores):
            st.write(f"Rank {i + 1}: Resume Name: {resume_name} - Similarity: {score}%")
