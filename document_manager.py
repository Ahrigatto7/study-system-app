import fitz  # PyMuPDF
import pandas as pd
from konlpy.tag import Okt
from docx import Document

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_excel(file):
    df = pd.read_excel(file)
    return df.astype(str).apply(lambda x: " ".join(x), axis=1).str.cat(sep='\n')

def extract_text_from_txt(file):
    return file.read().decode("utf-8")

def extract_keywords(text, top_n=10):
    okt = Okt()
    nouns = okt.nouns(text)
    freq = pd.Series(nouns).value_counts()
    return freq.head(top_n).index.tolist()

def process_file(file, file_type):
    if file_type == "pdf":
        text = extract_text_from_pdf(file)
    elif file_type == "docx":
        text = extract_text_from_docx(file)
    elif file_type in ["xlsx", "xls"]:
        text = extract_text_from_excel(file)
    elif file_type == "txt":
        text = extract_text_from_txt(file)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다.")
    keywords = extract_keywords(text)
    return text, keywords