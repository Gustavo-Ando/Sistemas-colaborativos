from typing import Optional
from typing_extensions import TypedDict, Annotated

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AnyMessage, SystemMessage

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

# Cria uma classe para uma tarefa, contendo uma descrição, uma data e um responável (opcionais)
class Task:
    task: str
    responsible: Optional[str]
    date: Optional[str]

    def __init__(self, task, responsible, date):
        self.task = task
        self.responsible = responsible
        self.date = date
    
    def __str__(self):
        return f"({self.task}, {self.responsible}, {self.date})"

    def get_task(self):
        return self.task
        
    def get_resp(self):
        return self.responsible
    
    def get_date(self):
        return self.date

# Cria a lista de tarefas
task_list: list[Task] = []


# Define o State
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Função utilizada para imprimir a lista de tarefas atual
def task_to_str() -> str:
    result = "=== Current task list ===\n"
    for task in task_list:
        result += "* " + str(task.get_task()) + "\n"
        if(task.get_date() is not None): 
            result += "    -> Date: " + str(task.get_date()) + "\n"
        else:
            result += "    -> Date: --\n"
        if(task.get_resp() is not None):
            result += "    -> Responsible: " + str(task.get_resp()) + "\n"
        else:
            result += "    -> Responsible: --\n"

    result += "=======================\n"
    return result

# Tool: Print list
@tool
def print_task_list() -> str:
    """
    This function can be used to print the current task list
    """
    return task_to_str()
    
# Tool: Adiciona tarefas à list, com responsável e data (opcionais)
@tool
def add_to_task_list(task: str, responsible: Optional[str], date: Optional[str]) -> str:
    """
    This function adds a new task to the task list
    
    Args:
        task: task to be added (Only task, without information about date or person responsible)
        responsible: person responsible for task (can be None if not known)
        date: date of task (can be None if not known)
    """
    task_list.append(Task(task=task,responsible=responsible,date=date))
    return task_to_str()

# Inicializa o chat model
llm = ChatOllama(model="gpt-oss")

# Fornece as tools ao model
llm_with_tools = llm.bind_tools([add_to_task_list, print_task_list])

# Função para chamar as tools no grafo
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Cria o grafo com o nó de tools e o responsável por chamá-las
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([add_to_task_list, print_task_list]))

builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", END)
graph = builder.compile()

# Visualização do grafo
graph.get_graph().draw_mermaid_png(output_file_path="./img.png")
print("Generated graph")

# Input do usuário
messages = {"messages": [SystemMessage(content="You are an agent that should check if the user or someone else plans to do something, and if so, add to task list. If they want to check the list, you must print it. DO NOT ANSWER ANYTHING ELSE.")]}
user_input = input()
while user_input != "exit":
    messages["messages"].append(HumanMessage(content=user_input, name="User"))
    messages = graph.invoke(messages)
    for m in messages['messages']:
        m.pretty_print()
    user_input = input()
