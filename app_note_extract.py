import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
import os
from note_manager import save_note

st.title("📚 Concept & Case Extractor (with Font Size)")

uploaded_files = st.file_uploader("📤 Upload PDF Documents", type="pdf", accept_multiple_files=True)

if uploaded_files:
    file_names = [file.name for file in uploaded_files]
    selected_file_name = st.selectbox("🔽 Select a document to analyze", file_names)

    selected_file = next((f for f in uploaded_files if f.name == selected_file_name), None)

    if selected_file:
        doc = fitz.open(stream=selected_file.read(), filetype="pdf")

        concepts = set()
        cases = []

        for page in doc:
            text = page.get_text()

            # 사례 추출
            case_matches = re.findall(r'<사례\s*(\d+)>[\s\n]*([^\n]+)', text)
            for number, title in case_matches:
                cases.append({
                    'Case Number': int(number),
                    'Title': title.strip(),
                    'Summary': '',
                    'Extracted Keywords': ''
                })

            # 개념 추출: 1) 패턴 기반
            pattern_concepts = re.findall(r'(?:\d+\.\s*|●\s*|▶\s*)([가-힣A-Za-z\(\)]+)\s*\n', text)
            for c in pattern_concepts:
                c = c.strip()
                if len(c) > 1:
                    concepts.add(c)

            # 개념 추출: 2) 글씨 크기 기반
            dict_text = page.get_text("dict")
            for block in dict_text["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = span.get("size", 0)
                            text = span.get("text", "").strip()
                            if len(text) > 1 and size >= 14:
                                concepts.add(text)

        # 결과 정리
        concept_df = pd.DataFrame(sorted(concepts), columns=["Concept"])
        case_df = pd.DataFrame(cases)

        st.subheader("📌 Extracted Concepts")
        st.dataframe(concept_df)

        st.subheader("📎 Extracted Cases")
        st.dataframe(case_df)

        # 노트로 저장
        if st.button("📝 Save Concepts as Note"):
            summary = "\n".join(concept_df['Concept'].tolist())
            save_note(
                title=f"Concepts from {selected_file_name}",
                content=summary,
                tags="concepts,auto",
                filename=selected_file_name,
                category="Extracted"
            )
            st.success("✅ Concepts saved to notes.")

        if st.button("📝 Save Cases as Note"):
            summary = "\n".join([f"{r['Case Number']}. {r['Title']}" for _, r in case_df.iterrows()])
            save_note(
                title=f"Cases from {selected_file_name}",
                content=summary,
                tags="cases,auto",
                filename=selected_file_name,
                category="Extracted"
            )
            st.success("✅ Cases saved to notes.")