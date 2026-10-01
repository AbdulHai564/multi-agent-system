from typing import TypedDict
from langgraph.graph import StateGraph, END
from tools.rag_tools import bm25_retrieval, sementic_retrieval, hybrid_search, cohere_reranker, generate_answer

class RAGState(TypedDict):
    question: str
    chunks: list
    docs: list
    answer: str

def retrieve(state):
    bm25 = bm25_retrieval(state["chunks"])
    semantic = sementic_retrieval()
    hybrid_results = hybrid_search(state["question"], bm25, semantic, state["chunks"])
    state["docs"] = cohere_reranker(hybrid_results, state["question"])
    return state

def generate(state):
    if state["docs"]:
        state["answer"] = generate_answer(state["docs"], state["question"])
    else:
        state["answer"] = "I couldn't find anything relevant in this PDF."
    return state

def build_rag_agent():
    graph = StateGraph(RAGState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

def ask_pdf(agent, question, chunks):
    result = agent.invoke({
        "question": question,
        "chunks": chunks,
        "docs": [],
        "answer": ""
    })
    return result["answer"]