from typing import Annotated, TypedDict, Optional
from operator import add as add_messages
from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage, HumanMessage, AnyMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

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

def build_llm(temperature: float = 0):
    return ChatOllama(model="gpt-oss", temperature=temperature)

def build_agent(llm):
    # Função utilizada para imprimir a lista de tarefas atual
    def task_to_str() -> str:
        result = "≡≡≡≡≡ Current task list ≡≡≡≡≡\n\n"
        for i, task in enumerate(task_list):
            result += f"{i+1}. " + str(task.get_task()) + "\n\n"
            if(task.get_date() is not None): 
                result += "    -> Date: " + str(task.get_date()) + "\n\n"
            else:
                result += "    -> Date: --\n\n"
            if(task.get_resp() is not None):
                result += "    -> Responsible: " + str(task.get_resp()) + "\n\n"
            else:
                result += "    -> Responsible: --\n\n"
    
        result += "≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡\n"
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
    
    @tool
    def remove_from_task_list(task: str, responsible: Optional[str], date: Optional[str]) -> str:
        '''
        This function removes a task from the task list when it's completed.
    
        Args:
            task: task to be removed
            responsible: person responsible for the task that is going to be removed (can be None)
            date: date of the task that is going to be removed (can be None)
        '''
        class Answer(BaseModel):
            index: int = Field(description="Index of task")
        llm_temp = ChatOllama(model="gpt-oss").with_structured_output(Answer)
    
        task_str = task + "\n"
        if responsible is not None:
            task_str += "    -> Responsible: " + responsible + "\n"
        if date is not None:
            task_str += "    -> Date: " + date + "\n"
            
        resultado = llm_temp.invoke([SystemMessage(f"Given the following task list: \n{task_to_str()}\n identify the index of the given task, answer only with the number."), HumanMessage(f"What's the index of the following task?\n {task_str}")])
        task_list.pop(resultado.index - 1)
        return task_to_str()
    
    llm_with_tools = llm.bind_tools([add_to_task_list, print_task_list, remove_from_task_list])

    # Define o State
    class MessagesState(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    def tool_calling_llm(state: MessagesState) -> MessagesState:
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
    # Cria o grafo com o nó de tools e o responsável por chamá-las
    builder = StateGraph(MessagesState)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode([add_to_task_list, print_task_list, remove_from_task_list]))
    
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition,
    )
    builder.add_edge("tools", END)
    return builder.compile()
