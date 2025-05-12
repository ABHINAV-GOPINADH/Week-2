import streamlit as st
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_with_fallback(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text += page_text
            else:
                # OCR fallback
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                ocr_text = pytesseract.image_to_string(img)
                text += ocr_text
    return text

# Streamlit app
st.title("📄 PDF Text Extractor with OCR Fallback")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ PDF uploaded successfully!")

    file_bytes = uploaded_file.read()
    extracted_text = extract_text_with_fallback(file_bytes)

    if extracted_text.strip():
        st.subheader("📜 Extracted Text:")
        st.text_area("PDF Text", value=extracted_text, height=400)

        # Optional: Download button
        st.download_button("📥 Download Text", extracted_text, file_name="extracted_text.txt")
    else:
        st.warning("⚠️ No text found in the PDF.")
