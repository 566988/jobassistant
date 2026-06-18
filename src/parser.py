import io
import PyPDF2
import docx

def extract_text_from_pdf(file) -> str:
    try:
        file.seek(0)
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    except Exception as e:
        raise ValueError(f"PDF 解析失败: {e}")

def extract_text_from_docx(file) -> str:
    try:
        # 使用 getvalue() 获取字节流，兼容所有 Streamlit 版本
        file_bytes = file.getvalue()
        doc = docx.Document(io.BytesIO(file_bytes))
        text = "\n".join([para.text for para in doc.paragraphs])
        if not text.strip():
            raise ValueError("DOCX 文件中未提取到文本，请检查文件内容")
        return text.strip()
    except Exception as e:
        raise ValueError(f"DOCX 解析失败: {e}")

def parse_resume(uploaded_file) -> str:
    if uploaded_file is None:
        return ""
    file_type = uploaded_file.name.split(".")[-1].lower()
    if file_type == "pdf":
        return extract_text_from_pdf(uploaded_file)
    elif file_type == "docx":
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("不支持的文件类型，请上传 PDF 或 DOCX")
