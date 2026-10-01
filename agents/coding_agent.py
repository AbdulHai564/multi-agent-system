from typing import TypedDict

from langgraph.graph import END, StateGraph
from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from tools.coding_tools import execute_code


class CodingState(TypedDict):
    task: str
    code: str
    output: str
    error: bool
    retries: int


def _clean_code(text: str) -> str:
    code = text.strip()
    if code.startswith("```"):
        lines = code.splitlines()
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines).strip()
    return code


def write_code(state: CodingState) -> CodingState:
    llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
    if state["retries"] > 0:
        prompt = f"""Fix the Python code for this task. Return only executable Python code, without Markdown fences.

Task:
{state['task']}

Previous code:
{state['code']}

Execution output/error:
{state['output']}
"""
    else:
        prompt = f"""Write executable Python code for this task. Return only Python code, without Markdown fences.

Task: {state['task']}
"""

    result = llm.invoke(prompt)
    state["code"] = _clean_code(str(result.content))
    return state


def execute(state: CodingState) -> CodingState:
    state["output"] = execute_code(state["code"])
    return state


def check_error(state: CodingState) -> CodingState:
    state["error"] = "Errors:" in state["output"]
    if state["error"]:
        state["retries"] += 1
    return state


def should_retry(state: CodingState) -> str:
    if state["error"] and state["retries"] < 3:
        return "write_code"
    return END


def build_coding_agent():
    graph = StateGraph(CodingState)
    graph.add_node("write_code", write_code)
    graph.add_node("execute", execute)
    graph.add_node("check_error", check_error)
    graph.set_entry_point("write_code")
    graph.add_edge("write_code", "execute")
    graph.add_edge("execute", "check_error")
    graph.add_conditional_edges("check_error", should_retry)
    return graph.compile()


def run_coding(task: str) -> dict[str, str]:
    agent = build_coding_agent()
    result = agent.invoke(
        {
            "task": task,
            "code": "",
            "output": "",
            "error": False,
            "retries": 0,
        }
    )
    return {"code": result["code"], "output": result["output"]}
