
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from document_manager import process_file
from summary_generator import generate_summary
from note_manager import save_note, load_notes
from progress_tracker import update_progress, get_progress_report

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="Dashboard", layout="wide")
st.image("static/logo.png", width=100)
st.title("📚 Dashboard")

menu = st.sidebar.radio("Select Menu", [
    "📚 Extract Concepts/Cases",
    "📘 Language Translator",
    "📒 View Notes",
    "➕ New Note",
    "📤 Upload File",
    "📊 Progress Tracker"
])

if menu == "📘 Language Translator":
    st.header("🌐 GPT 한국어 ↔ 영어 ↔ 한자 변환기")
    input_text = st.text_area("📝 Enter the text to translate", placeholder="e.g., A wise person saves their words")
    target_lang = st.selectbox("🌍 Select target language", ["영어", "한자", "한국어로 해석"])
    if st.button("🔁 변환하기"):
        if input_text.strip():
            prompt = f"다음을 {target_lang}로 번역해 주세요: '{input_text}'"
            with st.spinner("GPT is translating..."):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                st.success("✅ Translation complete")
                st.text_area("🔤 Result", result, height=150)
        else:
            st.warning("Please enter a sentence.")

elif menu == "📒 View Notes (Editable)":
    st.header("📒 View and Edit Notes")
    notes = load_notes()
    if notes.empty:
        st.info("No notes have been created.")
    else:
        for _, row in notes.iterrows():
            st.markdown(f"""
                <div style='background-color:#fff8f5;padding:1rem;margin:1rem 0;border-radius:1rem;border:1px solid #eee;'>
                    <strong>{row['title']}</strong><br>
                    <p>{row['content']}</p>
                    <span style='color:gray;'>#{row['tags']}</span>
                </div>
            """, unsafe_allow_html=True)

elif menu == "➕ New Note":
    st.header("✍️ Create a New Note")
    title = st.text_input("Title")
    content = st.text_area("Content", height=200)
    tags = st.text_input("Tags (comma-separated)")
    if st.button("저장"):
        save_note(title, content, tags)
        st.success("Note has been saved.")

elif menu == "📤 Upload File":
    st.header("📁 Document Upload and Auto Summary")
    file = st.file_uploader("Upload PDF, DOCX, XLSX, or TXT", type=["pdf", "docx", "xlsx", "xls", "txt"])
    if file:
        ext = file.name.split(".")[-1]
        text, keywords = process_file(file, ext)
        summary = generate_summary(text)
        st.text_area("📋 GPT 요약 Result", summary, height=300)
        if st.button("Save as Note"):
            save_note(file.name, summary, ",".join(keywords))
            st.success("Note saved successfully!")

elif menu == "📊 Progress Tracker":
    st.header("📈 Study Progress Management")
    topic = st.text_input("Topic")
    percent = st.slider("Progress (%)", 0, 100)
    if st.button("Save Progress"):
        update_progress(topic, percent)
        st.success("Save Progress 완료!")
    st.subheader("📊 Progress Overview")
    st.dataframe(get_progress_report())  # 진도 관리 그대로 유지



elif menu == "🤖 HF Chatbot":
    st.header("🤖 Hugging Face GPT-style Chatbot (Free Model)")
    hf_token = os.getenv("HF_API_TOKEN")
    if not hf_token:
        st.error("Please add HF_API_TOKEN in your .env file.")
    else:
        # 모델 선택
        model_choice = st.selectbox("🧠 Choose a model", [
            "HuggingFaceH4/zephyr-7b-beta",
            "mistralai/Mistral-7B-Instruct-v0.1",
            "tiiuae/falcon-7b-instruct"
        ])

        # 상태 초기화
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        if "topic_history" not in st.session_state:
            st.session_state.topic_history = []

        # 사용자 입력
        prompt = st.text_input("💬 Ask your question", key="user_input")

        if st.button("🚀 Send"):
            if prompt.strip() == "":
                st.warning("Please enter a question.")
            else:
                # 대화 저장
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                st.session_state.topic_history.append(prompt[:40])

                # Hugging Face API 호출
                import requests
                API_URL = f"https://api-inference.huggingface.co/models/{model_choice}"
                headers = { "Authorization": f"Bearer {hf_token}" }
                payload = { "inputs": prompt, "parameters": { "max_new_tokens": 200 } }
                with st.spinner("🤖 Generating response..."):
                    res = requests.post(API_URL, headers=headers, json=payload)
                    if res.status_code == 200:
                        result = res.json()[0]["generated_text"]
                        st.session_state.chat_history.append({"role": "bot", "content": result})
                    else:
                        result = f"Error: {res.status_code}"
                        st.session_state.chat_history.append({"role": "bot", "content": result})

        # 대화 출력
        if st.session_state.chat_history:
            st.markdown("### 💬 Chat History")
            for msg in st.session_state.chat_history[::-1]:
                speaker = "🧠 Bot" if msg["role"] == "bot" else "🙋 You"
                st.markdown(f"**{speaker}**: {msg['content']}")

        # 토픽 출력
        if st.session_state.topic_history:
            st.markdown("### 📚 Asked Topics")
            for i, topic in enumerate(st.session_state.topic_history[::-1]):
                st.markdown(f"- {i+1}. {topic}")


elif menu == "📚 Extract Concepts/Cases":
    st.header("📚 Concept & Case Extractor (with Font Size)")

    uploaded_files = st.file_uploader("📤 Upload PDF Documents", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        file_names = [file.name for file in uploaded_files]
        selected_file_name = st.selectbox("🔽 Select a document to analyze", file_names)

        selected_file = next((f for f in uploaded_files if f.name == selected_file_name), None)

        if selected_file:
            import fitz
            import re
            import pandas as pd
            from note_manager import save_note

            doc = fitz.open(stream=selected_file.read(), filetype="pdf")

            concepts = set()
            cases = []

            for page in doc:
                text = page.get_text()
                case_matches = re.findall(r'<사례\s*(\d+)>[\s\n]*([^\n]+)', text)
                for number, title in case_matches:
                    cases.append({
                        'Case Number': int(number),
                        'Title': title.strip(),
                        'Summary': '',
                        'Extracted Keywords': ''
                    })

                pattern_concepts = re.findall(r'(?:\d+\.\s*|●\s*|▶\s*)([가-힣A-Za-z\(\)]+)\s*\n', text)
                for c in pattern_concepts:
                    c = c.strip()
                    if len(c) > 1:
                        concepts.add(c)

                dict_text = page.get_text("dict")
                for block in dict_text["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                size = span.get("size", 0)
                                text = span.get("text", "").strip()
                                if len(text) > 1 and size >= 14:
                                    concepts.add(text)

            concept_df = pd.DataFrame(sorted(concepts), columns=["Concept"])
            case_df = pd.DataFrame(cases)

            
            st.subheader("📌 Extracted Concepts")
            concept_df = st.data_editor(concept_df, use_container_width=True, num_rows="dynamic")

            st.subheader("📎 Extracted Cases")
            case_df = st.data_editor(case_df, use_container_width=True, num_rows="dynamic")


            st.subheader("📎 Extracted Cases")
            st.dataframe(case_df)

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