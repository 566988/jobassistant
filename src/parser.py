import io
import PyPDF2
import docx

def extract_text_from_pdf(file) -> str:
    file.seek(0)
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file) -> str:
    file.seek(0)
    file_bytes = io.BytesIO(file.read())
    doc = docx.Document(file_bytes)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload PDF or DOCX.")
