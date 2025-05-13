import streamlit as st
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    """Extract text from the uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks with optional overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return chunks

# Streamlit UI
st.title("📄 PDF Uploader & Text Chunker")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    text = extract_text_from_pdf(uploaded_file)
    st.subheader("📜 Extracted Text (First 1000 chars)")
    st.write(text[:1000] + "..." if len(text) > 1000 else text)

    chunk_size = st.slider("Chunk size (characters)", 100, 2000, 500, 100)
    overlap = st.slider("Overlap (characters)", 0, 500, 50, 10)

    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)

    st.subheader(f"🧩 {len(chunks)} Chunks")
    for i, chunk in enumerate(chunks[:5]):  # Display only first 5 chunks
        st.text_area(f"Chunk {i+1}", chunk, height=150)
