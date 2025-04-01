import streamlit as st
from prompts import *
from utils import ExtractPDF, ExtractDoc, SendRequest, CreatePDF
import docx
from pathlib import Path
import os


# Streamlit App Layout Configuration
st.set_page_config(page_title="Resume Analyzer", layout="wide")

# App title and description
st.title("Resume Analyzer")
st.markdown("Optimize your resume with AI-driven insights and personalized feedback!")

# Sidebar for navigation and options
st.sidebar.markdown(
    """
    ---
    <p style="text-align: center; font-size: 20px; color: #888;">
        <small>Created by <a href="https://www.linkedin.com/in/monika-sharma-2878bb14/" target="_blank" style="color: #0078D4;">Monika Sharma</a></small>
    </p>
    """,
    unsafe_allow_html=True
)
st.sidebar.header("Navigation")
st.sidebar.markdown("""
    - **Job Description Input**: Paste the job description you're applying to.
    - **Resume Upload**: Upload your resume in PDF or Docx format for analysis.
    - **Analysis Options**: Use the buttons to get valuable insights and suggestions.
""")




# Left Column - User Inputs (Job Description and Resume)
with st.container():
    st.header("Job Description & Resume")
    jd_input = st.text_area(
        "Enter Job Description", 
        placeholder="Paste the job description here.", 
        key="text",
        height=150,
        help="Paste the job description for the position you're applying for."
    )
    
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf", "docx"], label_visibility="collapsed")
    if uploaded_file:
        st.success("Resume uploaded successfully!")

# Middle Section: Action Buttons
st.header("AI-Generated Insights & Feedback")
st.markdown(
    "<p style='font-size:14px; color:#777;'>Click on the buttons below to get actionable insights and recommendations.</p>",
    unsafe_allow_html=True
)

# Buttons to trigger actions
with st.expander("Resume Analysis Options"):
    submit1 = st.button("Job Description Insights")
    submit2 = st.button("Skills Gap Analysis")
    submit3 = st.button("Resume Percentage Match")
    submit4 = st.button("ATS Compatibility Check")
    submit5 = st.button("Resume Feedback")
    submit6 = st.button("Generate Optimized Resume")
    submit7 = st.button("Generate Cover Letter")



# Function to generate the response based on button clicked
def generate_response(prompt):
    if uploaded_file is not None:
        filename = uploaded_file.name  # Extract filename as a string
        file_extension = Path(filename).suffix  # Get file extension)
        
        # Extract text content from the uploaded PDF resume
        if file_extension == ".pdf":
            pdf_content = ExtractPDF(uploaded_file)
            response = SendRequest(jd_input, pdf_content, prompt)
        # Extract text content from the uploaded docx resume
        if file_extension == ".docx":
            doc_content = ExtractDoc(uploaded_file)
            response = SendRequest(jd_input, doc_content, prompt)
                
        # Display the response from AI
        st.subheader("Generated Response:")
        st.write(response)
    else:
        st.warning("Please upload a resume to proceed!")

# Function to generate the optimized PDF based on button clicked
def generate_pdf(prompt):
    if uploaded_file is not None:
        filename = uploaded_file.name  # Extract filename as a string
        file_extension = Path(filename).suffix  # Get file extension)
        
        if file_extension == ".pdf":
            pdf_content = ExtractPDF(uploaded_file)
            optimized_text = SendRequest(jd_input, pdf_content, prompt)
        # Extract text content from the uploaded docx resume
        if file_extension == ".docx":
            doc_content = ExtractDoc(uploaded_file)
            optimized_text = SendRequest(jd_input, doc_content, prompt)
                
        # Generate the optimized PDF file
        input_filename = uploaded_file.name.split('.')[0]  # Get the original filename
        optimized_filename = CreatePDF(optimized_text, input_filename)
        
        if optimized_filename:
            with open(optimized_filename, "rb") as file:
                st.download_button("Click Here to Download Generated File", file, file_name=optimized_filename)
        else: 
            st.error("There was an issue generating the optimized resume.")
    else:
        st.warning("Please upload a resume to proceed!")

# Button Logic to trigger respective analysis
if submit1:
    generate_response(prompt1)
elif submit2:
    generate_response(prompt2)
elif submit3:
    generate_response(prompt3)
elif submit4:
    generate_response(prompt4)
elif submit5:
    generate_response(prompt5)
elif submit6:
    generate_pdf(prompt6)
elif submit7:
    generate_pdf(prompt7)