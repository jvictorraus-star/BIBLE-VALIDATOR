import streamlit as st
import google.generativeai as genai
import os
from PyPDF2 import PdfReader

# 1. Setup & Title
st.set_page_config(page_title="Biblical History Validator", page_icon="📜")
st.title("📜 Biblical History Validator")
st.markdown("---")

# 2. Sidebar for Configuration
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    uploaded_files = st.file_uploader("Upload Historical PDFs", type="pdf", accept_multiple_files=True)

# 3. Function to Extract Text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# 4. The "Historian" Brain Logic
if api_key and uploaded_files:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Process the documents
    raw_text = get_pdf_text(uploaded_files)
    
    # User Input
    user_question = st.text_input("Ask a historical question (e.g., 'Why was Maccabees removed?'):")
    
    if user_question:
        # THE GUARDRAIL PROMPT: This forces the AI to stay factual
        prompt = f"""
        CONTEXT FROM HISTORICAL DOCUMENTS:
        {raw_text[:15000]} 
        
        USER QUESTION: {user_question}
        
        INSTRUCTIONS:
        You are a secular, neutral historian. Use ONLY the provided context to answer. 
        1. If the answer is not in the text, say 'Historical evidence for this is not present in my database.'
        2. Strip away all emotional, religious, or devotional language. 
        3. Do not offer spiritual advice. 
        4. Focus on dates, councils, and manuscript names (Septuagint, Masoretic, etc.).
        """
        
        response = model.generate_content(prompt)
        st.subheader("Historical Fact-Check:")
        st.write(response.text)
else:
    st.info("Please enter your API Key and upload your historical documents to begin.")
