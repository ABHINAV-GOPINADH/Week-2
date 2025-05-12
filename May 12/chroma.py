import streamlit as st
import chromadb
import fitz  # PyMuPDF for PDF extraction
import tempfile

# Initialize the ChromaDB client
client = chromadb.Client()

# Collection name
collection_name = "pdf_collection"

# Attempt to get the collection or create it if not found
try:
    collection = client.get_collection(collection_name)
    st.write("Collection 'pdf_collection' found!")
except chromadb.errors.NotFoundError:
    st.write("Collection not found, creating a new one...")
    collection = client.create_collection(collection_name)
    st.write("New collection created!")

def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_path = temp_file.name

    doc = fitz.open(temp_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def add_pdf_to_chromadb(pdf_text):
    collection.add(
        documents=[pdf_text],
        metadatas=[{"source": "PDF"}],
        ids=["pdf_doc"]
    )
    st.success("✅ PDF text added to ChromaDB successfully!")

def retrieve_pdf_from_chromadb():
    results = collection.get()
    return results["documents"]

def main():
    st.title("📄 PDF to ChromaDB")

    # Upload PDF
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

    # Initialize session_state for pdf_text
    if "pdf_text" not in st.session_state:
        st.session_state.pdf_text = None

    if pdf_file is not None:
        st.write("📃 Extracting text from the PDF...")
        st.session_state.pdf_text = extract_text_from_pdf(pdf_file)
        st.text_area("Extracted PDF Text", st.session_state.pdf_text, height=300)

    if st.session_state.pdf_text:
        if st.button("Add to ChromaDB"):
            add_pdf_to_chromadb(st.session_state.pdf_text)

    # ✅ Always show the verify button
    if st.button("Verify Data in ChromaDB"):
        st.write("🔍 Verifying data in ChromaDB...")
        documents = retrieve_pdf_from_chromadb()
        if documents:
            st.subheader("Stored Documents in ChromaDB:")
            for doc in documents:
                st.text_area("Stored PDF Text", doc, height=300)
        else:
            st.warning("No documents found in ChromaDB.")

if __name__ == "__main__":
    main()
