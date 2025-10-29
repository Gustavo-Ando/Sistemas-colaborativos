# Sistema agêntico

## Como usar

Optamos por usar um LLM que roda localmente, assim primeiro será necessário baixá-lo com os seguintes passos:
```shell
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gpt-oss
```
Após isso, são necessários alguns pacotes do python, sendo recomendado criar um virtual environment para baixá-los com:
```shell
virtualenv venv
source venv/bin/activate
```
Os pacote necessários podem então ser baixados com:
```shell
pip install -U langchain_ollama langgraph 
```
Com todos esses requesitos instalados, para rodar o agente bastar fazer
```shell
python3 main.py
```
Para utilizá-lo, basta enviar mensagens simulando uma conversa em grupo com alocação de tarefas, que o agente irá atualizar uma lista quando necessário. Para terminar, basta enviar _exit_.

## Exemplo de funcionamento
Entrada:
```
I need to buy groceries
Hi! What day is it today?
What is currently on the task list?
John needs to visit his friends next week!
exit
```
Resultado final:
```
================================ Human Message =================================
Name: User

I need to buy groceries
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (d3f311b7-a4e3-4dd7-97fb-d7c285a517c0)
 Call ID: d3f311b7-a4e3-4dd7-97fb-d7c285a517c0
  Args:
    date: None
    responsible: None
    task: buy groceries
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
* buy groceries
    -> Date: --
    -> Responsible: --
=======================

================================ Human Message =================================
Name: User

Hi! What day is it today?
================================== Ai Message ==================================
================================ Human Message =================================
Name: User

What is currently on the task list?
================================== Ai Message ==================================
Tool Calls:
  print_task_list (9b7bb3c2-b4f5-459e-aafa-71843d610cec)
 Call ID: 9b7bb3c2-b4f5-459e-aafa-71843d610cec
  Args:
================================= Tool Message =================================
Name: print_task_list

=== Current task list ===
* buy groceries
    -> Date: --
    -> Responsible: --
=======================

================================ Human Message =================================
Name: User

John needs to visit his friends next week!
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (4a148d88-3d27-4d82-a85a-452bbc6a7ef3)
 Call ID: 4a148d88-3d27-4d82-a85a-452bbc6a7ef3
  Args:
    date: next week
    responsible: John
    task: visit friends
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
* buy groceries
    -> Date: --
    -> Responsible: --
* visit friends
    -> Date: next week
    -> Responsible: John
=======================
```
