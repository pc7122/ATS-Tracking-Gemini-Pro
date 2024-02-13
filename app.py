import os
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai


st.set_page_config(page_title='ATS Tracking', page_icon='🔮', layout='wide')
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])


def get_gemini_responce(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ''

    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()

    return text


input_prompt = """
    Hey Act Like a skilled or very experience ATS(Application Tracking System)
    with a deep understanding of tech field,software engineering,data science ,data analyst
    and big data engineer. Your task is to evaluate the resume based on the given job description.
    You must consider the job market is very competitive and you should provide 
    best assistance for improving thr resumes. Assign the percentage Matching based 
    on Jd and
    the missing keywords with high accuracy
    resume:{text}
    description:{jd}

    I want the response in following format:
    Mathching Percentage: 80%
    
    Missing Keywords:
    - Python
    - Java
    - Data Science
    
    profile summary:
    
"""

st.markdown("<style>h1 {text-align: center}</style>", unsafe_allow_html=True)
st.title('🔮 ATS Tracking using Google Gemini Pro')
st.divider()

col1, col2 = st.columns(2)

with col1:
    job_description = st.text_area('Enter the job description', height=500)

with col2:
    uploaded_file = st.file_uploader('Upload a PDF', type='pdf')
    submit = st.button('Submit', use_container_width=True)

if submit:
    pdf_text = input_pdf_text(uploaded_file)
    response = get_gemini_responce(
        input_prompt.format(text=pdf_text, jd=job_description))
    st.write(response)
