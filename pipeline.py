from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
      topic: str
      research_results: Annotated[List[str], operator.add]
      report: str
      feedback: str
      iteration: int

def search_node(state: AgentState):
      # This logic is handled in the Streamlit app.py for simplicity in this demo system
      return {"iteration": state.get("iteration", 0) + 1}

def writer_node(state: AgentState):
      return state

def critic_node(state: AgentState):
      return state

workflow = StateGraph(AgentState)
workflow.add_node("search", search_node)
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)

workflow.set_entry_point("search")
workflow.add_edge("search", "writer")
workflow.add_edge("writer", "critic")
workflow.add_edge("critic", END)

app = workflow.compile()
