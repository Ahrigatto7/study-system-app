PK     3|ąZ?ůs	  	     app.py
import streamlit as st
import pandas as pd
import uuid
import os
from dotenv import load_dotenv
from openai import OpenAI
from pyvis.network import Network
import streamlit.components.v1 as components
from note_manager import save_note, load_notes
from document_manager import process_file
from summary_generator import generate_summary
from progress_tracker import update_progress, get_progress_report

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="đ§  Unified Study App", layout="wide")
st.image("static/logo.png", width=100)
st.title("đ§  Dashboard")

menu = st.sidebar.radio("đ Menu", [
    "đ Language Translator",
    "đ¤ Upload File",
    "đ View Notes",
    "â New Note",
    "đ Extract Concepts/Cases",
    "đ Progress Tracker",
    "đ Graph Visualizer",
    "đ¤ HF Chatbot"
])

if menu == "đ Language Translator":
    st.header("đ Language Translator")
    input_text = st.text_area("Enter text to translate:")
    target_lang = st.selectbox("Target Language", ["English", "Korean", "Chinese"])
    if st.button("Translate"):
        prompt = f"Translate the following into {target_lang}:
{input_text}"
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        st.text_area("Translation Result", response.choices[0].message.content, height=200)

elif menu == "đ Graph Visualizer":
    st.header("đ Concept Graph")
    df_file = "graph_notes.csv"
    try:
        df = pd.read_csv(df_file)
    except:
        df = pd.DataFrame(columns=["Title", "LinkedTo"])

    with st.sidebar:
        t = st.text_input("Title", key="graph_title")
        linked = st.text_input("Linked To", key="graph_link")
        if st.button("Add Node"):
            df.loc[len(df)] = [t, linked]
            df.to_csv(df_file, index=False)

    net = Network(height="600px", width="100%", bgcolor="#fff", font_color="black")
    for _, row in df.iterrows():
        title = str(row["Title"]) if pd.notna(row["Title"]) else "Untitled"
        net.add_node(title, label=title)
        for link in str(row["LinkedTo"]).split(","):
            link = link.strip()
            if link:
                net.add_node(link, label=link)
                net.add_edge(title, link)

    net.save_graph("graph.html")
    components.html(open("graph.html").read(), height=650)
PK     3|ąZ?ůs	  	             ¤    app.pyPK      4   Ş	    