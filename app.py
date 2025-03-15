from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from PyPDF2 import PdfReader
import streamlit as st
import re

load_dotenv()

st.title("Text Summarization")

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",  
    max_new_tokens=256
)

selected = st.radio(label="",options=["Summarize PDF","Summarize text"]) 
if selected == "Summarize PDF":
    file = st.file_uploader(label="Upload your file")
    max_len = st.number_input(label="Max length for summarization", step=10, value=100)
    min_len = st.number_input(label="Min length for summarization", step=10, value=50)
    if file:
        reader = PdfReader(file)
        text = ""
        for i in reader.pages:
            text+=i.extract_text()
        llm.invoke("File Content")
if selected == "Summarize text":
    text = st.text_area(label="Input the text you want to summarize")
    max_len = st.number_input(label="Max length for summarization", step=10, value=100)
    min_len = st.number_input(label="Min length for summarization", step=10, value=50)

if st.button("Submit"):
    if text:
        prompt = f"Summarize the following text in between {max_len} and {min_len} lines:\n\n{text}"
        summary = llm.invoke(prompt)
        parts = re.split(r"(\$\$.*?\$\$|\$.*?\$)", summary)

        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):  
                st.latex(part)
            elif part.startswith("$") and part.endswith("$"): 
                st.latex(part)
            else:
                st.write(part)

    else:
        st.warning("Please enter some text to summarize.")

question = st.text_input("Enter your question")
if st.button("Get answer") and question:
    llm = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation"
    )
    output = llm.invoke(f"{text} answer the below question accurately based on the given information {question}")
    st.write(output)