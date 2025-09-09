import os
import streamlit as st
from groq import Groq
from docx import Document

from groq import Groq
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    st.error("Groq API key ontbreekt.")
    st.stop()

client = Groq(api_key=API_KEY)

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a documet below and ask a question about it – GPT will answer! "
)
# Let the user upload a file via `st.file_uploader`.
uploaded_file = st.file_uploader(
    "Upload a document (.txt, .md, .docx)", type=("txt", "md", "docx")
)

# Ask the user for a question via `st.text_area`.
question = st.text_area(
    "Now ask a question about the document!",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file,
)

if uploaded_file and question:

    # Process the uploaded file and question.
    if uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        document = "\n".join([para.text for para in doc.paragraphs])
    else:
        document = uploaded_file.read().decode()
        
    messages = [
        {
            "role": "user",
            "content": f"Here's a document: {document} \n\n---\n\n {question}",
        }
    ]

    # Generate an answer using the OpenAI API.
    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        stream=True,
    )

    # Stream the response to the app using `st.write_stream`.
    st.write_stream(stream)
