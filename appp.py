import os
import tempfile
import streamlit as st

from agents.coding_agent import build_coding_agent, run_coding
from agents.rag_agent import ask_pdf, build_rag_agent
from agents.deep_research_agent import build_research_agent, run_research
from tools.rag_tools import chunk_load, store

st.set_page_config(page_title="Multi-Agent System", layout="wide", page_icon="🤖")

@st.cache_resource
def get_coding_agent():
    return build_coding_agent()

@st.cache_resource
def get_rag_agent():
    return build_rag_agent()

@st.cache_resource
def get_research_agent():
    return build_research_agent()

# Session state
for key, default in {
    "active_agent": "cody",
    "chat_cody": [{"role": "agent", "content": "Hey. What are we building today."}],
    "chat_shakespeare": [],
    "chat_aristotle": [{"role": "agent", "content": "What can i research for you Today?"}],
    "pdf_loaded": False,
    "chunks": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Sidebar
with st.sidebar:
    st.title("Agents")
    st.divider()
    if st.button("🔴 Cody", use_container_width=True):
        st.session_state.active_agent = "cody"
    st.caption("Code execution")
    st.divider()
    if st.button("🔵 Shakespeare", use_container_width=True):
        st.session_state.active_agent = "shakespeare"
    st.caption("Document Q&A")
    st.divider()
    if st.button("🟣 Aristotle", use_container_width=True):
        st.session_state.active_agent = "aristotle"
    st.caption("Research")

# CODY
if st.session_state.active_agent == "cody":
    st.header("Cody — Code Execution")
    
    for msg in st.session_state.chat_cody:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                if "code" in msg:
                    st.write(msg.get("intro", ""))
                    st.code(msg["code"], language="python")
                    st.write("**Output:**", msg["output"])
                else:
                    st.write(msg["content"])

    user_input = st.chat_input("Tell Cody what to Build...")
    if user_input:
        st.session_state.chat_cody.append({"role": "user", "content": user_input})
        with st.spinner("Running..."):
            result = run_coding(user_input)
        st.session_state.chat_cody.append({
            "role": "agent",
            "intro": "There you go.",
            "code": result["code"],
            "output": result["output"],
        })
        st.rerun()

# SHAKESPEARE
elif st.session_state.active_agent == "shakespeare":
    st.header("Shakespeare — Document Q&A")

    if not st.session_state.pdf_loaded:
        uploaded = st.file_uploader("Please upload your PDF to get started", type=["pdf"])
        if uploaded:
            with st.spinner("Loading up"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
                    f.write(uploaded.read())
                    temp_path = f.name
                try:
                    chunks = chunk_load(temp_path)
                    store(chunks)
                finally:
                    os.unlink(temp_path)
                st.session_state.chunks = chunks
                st.session_state.pdf_loaded = True
                st.session_state.chat_shakespeare = [
                    {"role": "assitant", "content": "Loaded successfully. What do you want to know?"}
                ]
            st.rerun()
    else:
        if st.button("Upload new PDF"):
            st.session_state.pdf_loaded = False
            st.session_state.chunks = []
            st.session_state.chat_shakespeare = []
            st.rerun()

        for msg in st.session_state.chat_shakespeare:
            with st.chat_message("user" if msg["role"] == "user" else "assistant"):
                st.write(msg["content"])

        user_input = st.chat_input("chat with your document")
        if user_input:
            st.session_state.chat_shakespeare.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                answer = ask_pdf(get_rag_agent(), user_input, st.session_state.chunks)
            st.session_state.chat_shakespeare.append({"role": "assistant", "content": answer})
            st.rerun()

# ARISTOTLE
elif st.session_state.active_agent == "aristotle":
    st.header("Aristotle — Research")

    for msg in st.session_state.chat_aristotle:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.write(msg["content"])

    user_input = st.chat_input("Enter the Research Topic ")
    if user_input:
        st.session_state.chat_aristotle.append({"role": "user", "content": user_input})
        with st.spinner("Doing deep Research... Will be back with the completed Research in a moment "):
            output = run_research(user_input)
        st.session_state.chat_aristotle.append({"role": "assistant", "content": output})
        st.rerun()