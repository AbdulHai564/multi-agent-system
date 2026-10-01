# 🤖 Multi-Agent System

A LangGraph-powered AI assistant with three specialized agents, built with Groq, Tavily, Qdrant, E2B, and Streamlit.

🚀 **Live Demo:** [multi-agent-system-kd3gz4dqrpamrocypgeluj.streamlit.app](https://multi-agent-system-kd3gz4dqrpamrocypgeluj.streamlit.app)

---

## Agents

### 🔴 Cody — Code Execution
Writes Python code, executes it in a live E2B cloud sandbox, checks the output, and retries automatically if it errors. Built with a LangGraph feedback loop: `write → execute → check → retry`.

### 🔵 Shakespeare — Document Q&A
Upload any PDF and ask questions about it. Uses a hybrid BM25 + semantic search pipeline with Cohere reranking to find the most relevant chunks before generating an answer.

### 🟣 Aristotle — Deep Research
Give it any research topic and it autonomously searches the web, extracts page content, summarizes each source, and writes a structured report.

---

## Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph |
| LLM | Groq (`openai/gpt-oss-120b`) |
| Web search | Tavily |
| Vector store | Qdrant Cloud |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| Reranker | Cohere `rerank-english-v3.0` |
| BM25 retrieval | LangChain Classic |
| Code sandbox | E2B |
| UI | Streamlit |

---

## Setup

1. Clone the repo
```bash
git clone https://github.com/AbdulHai564/multi-agent-system.git
cd multi-agent-system
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys
```
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
QDRANT_URL=your_url
QDRANT_API_KEY=your_key
COHERE_API_KEY=your_key
E2B_API_KEY=your_key
COLLECTION_NAME=your_collection
```

4. Run the app
```bash
streamlit run appp.py
```

---

## Project Structure

```
multi-agent-system/
├── .env
├── requirements.txt
├── config.py
├── agents/
│   ├── coding_agent.py
│   ├── deep_research_agent.py
│   └── rag_agent.py
├── tools/
│   ├── coding_tools.py
│   ├── rag_tools.py
│   └── search_tools.py
└── appp.py
```

---

## Note
This project uses free-tier APIs. Expect 30–60 second response times, especially for Aristotle (6 LLM calls per research task) and Cody (E2B sandbox cold start).

---

Built by [Abdulhai](https://github.com/AbdulHai564)
