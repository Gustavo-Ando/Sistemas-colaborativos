# Sistemas Colaborativos - Trabalho Final

Professor: 
Autores:

## Cenário Colaborativo
  O cenário pensado é um chat em grupo, no qual o agente iria ler as mensagens e organizar as tarefas que devem ser realizadas, assim como quem está responsável por fazê-las e sua data limite. Dessa forma, o nosso sistema agêntico seria para uso genérico em qualquer situação em grupo, para facilitar a coordenação e alocação de deveres.
  
  Ainda, esse agente em geral não interagiria diretamente com o chat, sendo apenas responsável por resumir as informações que os próprios usuários trariam em uma lista de tarefas.
  
## Diagrama do Grafo
Abaixo seguem as representações do Grafo do Sistema Agêntico.

![LangGraph](img.png)

![Diagrama](diagrama.png)

## Abordagem dos 3C

  O agente auxilia na **comunicação** entre os participantes do grupo, resumindo e condensando as tarefas alocadas e seus responsáveis em uma única lista de fácil visualização. A partir dessa mesma lista, os participantes também se beneficiam na **colaboração**, visto que, com ela, cada um sabe o que deve ser feito para que os objetivos em comum possam ser alcançados. Ainda, no quesito **coordenação**, o agente facilita a divisão das tarefas entre os membros do grupo, de forma organizada e sistemática.
  
  Nesse contexto, a LLM tem um papel fundamental, sendo necessária para entender e processar a linguagem natural de forma a entender quais tarefas estão sendo alocadas pelo grupo, quais seus prazos e quem está responsável por cada uma.
  
  Uma possível forma de expansão do sistema seria incluir prioridades junto às tarefas, e assim adicionar lembretes para as pessoas alocadas nelas quando perto de expirarem, assim como alertas caso excedam seu prazo. Com esse mesmo intuito, tarefas sem responsáveis alocadas poderiam receber lembretes após um período para que alguém as iniciasse.

## Sistema agêntico

### Como usar

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
Alice: Hey! How are you guys doing?
Bob: Hi! I need to finish the spreadsheet until Monday!
Alice: Ok, Charlie will write the report by next week too.
Charile: Actually, I already finished the report!
Bob: Nice! So what's the current task list?
exit
```
Resultado final:
```
================================ Human Message =================================
Name: User

Alice: Hey! How are you guys doing?
================================== Ai Message ==================================
================================ Human Message =================================
Name: User

Bob: Hi! I need to finish the spreadsheet until Monday!
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (ccf5dc00-7249-40c3-825c-f085bf90f246)
 Call ID: ccf5dc00-7249-40c3-825c-f085bf90f246
  Args:
    date: Monday
    responsible: Bob
    task: Finish spreadsheet
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
=======================

================================ Human Message =================================
Name: User

Alice: Ok, Charlie will write the report by next week too.
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (a6675373-b623-4eef-a8a9-00c6aca49f61)
 Call ID: a6675373-b623-4eef-a8a9-00c6aca49f61
  Args:
    date: next week
    responsible: Charlie
    task: Write report
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
2. Write report
    -> Date: next week
    -> Responsible: Charlie
=======================

================================ Human Message =================================
Name: User

Charile: Actually, I already finished the report!
================================== Ai Message ==================================
Tool Calls:
  remove_from_task_list (c2dbde44-b191-454b-a01a-e6bb476b9d60)
 Call ID: c2dbde44-b191-454b-a01a-e6bb476b9d60
  Args:
    date: next week
    responsible: Charlie
    task: Write report
================================= Tool Message =================================
Name: remove_from_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
=======================

================================ System Message ================================

You are an agent that should check if the user or someone else plans to do something, and if so, add to task list. If they want to check the list, you must print it. DO NOT ANSWER ANYTHING ELSE.
================================ Human Message =================================
Name: User

Alice: Hey! How are you guys doing?
================================== Ai Message ==================================
================================ Human Message =================================
Name: User

Bob: Hi! I need to finish the spreadsheet until Monday!
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (ccf5dc00-7249-40c3-825c-f085bf90f246)
 Call ID: ccf5dc00-7249-40c3-825c-f085bf90f246
  Args:
    date: Monday
    responsible: Bob
    task: Finish spreadsheet
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
=======================

================================ Human Message =================================
Name: User

Alice: Ok, Charlie will write the report by next week too.
================================== Ai Message ==================================
Tool Calls:
  add_to_task_list (a6675373-b623-4eef-a8a9-00c6aca49f61)
 Call ID: a6675373-b623-4eef-a8a9-00c6aca49f61
  Args:
    date: next week
    responsible: Charlie
    task: Write report
================================= Tool Message =================================
Name: add_to_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
2. Write report
    -> Date: next week
    -> Responsible: Charlie
=======================

================================ Human Message =================================
Name: User

Charile: Actually, I already finished the report!
================================== Ai Message ==================================
Tool Calls:
  remove_from_task_list (c2dbde44-b191-454b-a01a-e6bb476b9d60)
 Call ID: c2dbde44-b191-454b-a01a-e6bb476b9d60
  Args:
    date: next week
    responsible: Charlie
    task: Write report
================================= Tool Message =================================
Name: remove_from_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
=======================

================================ Human Message =================================
Name: User

Bob: Nice! So what's the current task list?
================================== Ai Message ==================================
Tool Calls:
  print_task_list (2c0975c0-ec81-4ac1-9e2c-cf38471d37c2)
 Call ID: 2c0975c0-ec81-4ac1-9e2c-cf38471d37c2
  Args:
================================= Tool Message =================================
Name: print_task_list

=== Current task list ===
1. Finish spreadsheet
    -> Date: Monday
    -> Responsible: Bob
=======================
```
