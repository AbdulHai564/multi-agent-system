from config import *
from tools.search_tools import search_web, extract_pages
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from typing import TypedDict

class ResearchState(TypedDict):
    query: str
    results: list
    extracted: list
    summaries: list
    final_report: str

def search(state):
    state["results"] = search_web(state["query"])
    return state

def extract(state):
    extracted = []
    for result in state["results"]:
        url = result["url"] if isinstance(result, dict) else result
        if not url:
            continue
        try:
            content = extract_pages(url)
        except Exception as e:
            print(f"Extract failed for {url}: {e}")
            continue
        if content:
            extracted.append(content)
    state["extracted"] = extracted
    return state

def summarize(state):
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
    summaries = []
    for content in state["extracted"]:
        truncated = content[:3000]  
        prompt = f"Summarize this content for deep research:\n\n{truncated}"
        summary = llm.invoke(prompt)
        summaries.append(summary.content)
    state["summaries"] = summaries
    return state

def report(state):
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
    summaries_text = "\n\n".join([s[:500] for s in state["summaries"]])
    prompt = f"""You are an excellent research analyst. Based on the summaries provided, make a detailed research report on query: {state["query"]}
Summaries: {summaries_text}
Create a structured report with your findings and conclusions."""
    result = llm.invoke(prompt)
    state["final_report"] = result.content
    return state



def build_research_agent():
    graph = StateGraph(ResearchState)
    graph.add_node("search", search)
    graph.add_node("extract", extract)
    graph.add_node("summarize", summarize)
    graph.add_node("report", report)
    graph.set_entry_point("search")
    graph.add_edge("search", "extract")
    graph.add_edge("extract", "summarize")
    graph.add_edge("summarize", "report")
    graph.add_edge("report", END)
    return graph.compile()

def run_research(query: str):
    agent = build_research_agent()
    result = agent.invoke({
        "query": query,
        "results": [],
        "extracted": [],
        "summaries": [],
        "final_report": ""
    })
    return result["final_report"]