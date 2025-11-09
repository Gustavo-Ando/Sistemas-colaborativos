# Sistemas Colaborativos - Trabalho Final

Autores:
|Nome|NUSP|
|----|-----|
|Gustavo Alvares Andó|15475345|
|Maria Clara de Souza Capato|15475294|

 Professor Moacir Antonelli Ponti

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
pip install -U langchain_ollama langgraph streamlit
```
Com todos esses requesitos instalados, para rodar o agente bastar fazer
```shell
python3 streamlit.py
```
Para utilizá-lo, primeiro é necessário criar um agente e então basta enviar mensagens simulando uma conversa em grupo com alocação de tarefas, que o agente irá atualizar uma lista quando necessário.

## Exemplo de funcionamento
Entrada:
```
Alice: Hey! How are you guys doing?
Bob: Hi! I need to finish the spreadsheet until Monday!
Alice: Ok, Charlie will write the report by next week too.
Charile: Actually, I already finished the report!
Bob: Nice! So what's the current task list?
```
Resultado final:
```
Alice: Hey! How are you guys doing?
Bob: Hi! I need to finish the spreadsheet until Monday!
Assistant:
    ≡≡≡≡≡ Current task list ≡≡≡≡≡
    1. Finish spreadsheet
        -> Date: Monday
        -> Responsible: Bob
    ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
Alice: Ok, Charlie will write the report by next week too.
Assistant:
    ≡≡≡≡≡ Current task list ≡≡≡≡≡
    1. Finish spreadsheet
        -> Date: Monday
        -> Responsible: Bob
    2. Write report
        -> Date: next week
        -> Responsible: Charlie
    ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
Charile: Actually, I already finished the report!
Assistant:
    ≡≡≡≡≡ Current task list ≡≡≡≡≡
    1. Finish spreadsheet
        -> Date: Monday
        -> Responsible: Bob
    ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
Bob: Nice! So what's the current task list?
Assistant:
    ≡≡≡≡≡ Current task list ≡≡≡≡≡
    1. Finish spreadsheet
        -> Date: Monday
        -> Responsible: Bob
    ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
```
