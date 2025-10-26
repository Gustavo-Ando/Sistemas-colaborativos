
from typing import TypedDict, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_core.messages import convert_to_messages

from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, MessagesState, START, END

llm = ChatOllama(model="llama3.2:1b")

class AgentState(TypedDict):
    messages: List[AIMessage | HumanMessage]
    task_list: List[str]

def mock_llm(state: AgentState) -> AgentState:
    answer = llm.invoke(state["messages"]).content
    state["messages"].append({"content": answer, "role": "ai", "name": "IA"})
    return state



'''


@tool
def update_task_list():
    
@tool
def 
'''

graph = StateGraph(AgentState)
#graph.add_node(alloc_llm)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
#graph.add_edge("mock_llm", "alloc_llm")
#graph.add_edge("alloc_llm", END)
graph = graph.compile()

user_msg = input()
result = {"messages": [], "task_list": []}
while user_msg != "exit":
    result["messages"].append({"role": "user", "content": user_msg, "name": "Eu"})
    result = graph.invoke(result)
    for msg in result["messages"]:
        print(f" * {msg["name"]}")
        print(msg["content"])
    print(" * Tasks: ")
    for task in result["task_list"]:
        print(task)
    print("-----------------------------------")
    user_msg = input()


