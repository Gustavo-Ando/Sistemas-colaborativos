import uuid
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage

from agent import (
    build_llm,
    build_agent,
)

USERS = ["Alice", "Bob", "Charlie", "David", "Eevee", "Frank"]

def ensure_session_state():
    """Initialize all session variables"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = {"messages": [SystemMessage(content="You are an agent that should check if the user or someone else plans to do something, and if so, add to task list. If they want to check the list, you must print it. DO NOT ANSWER ANYTHING ELSE.")]}
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = USERS[0]


def main():
    st.set_page_config(page_title="Sistema Colaborativo", page_icon="📄")
    ensure_session_state()

    st.title("📄 Sistema Colaborativo - Tasklist")
    st.caption("Feel free to chat and talk about your tasks here! The model will create a tasklist for you.")

    with st.sidebar:

        st.header("User")
        st.session_state.selected_user = st.selectbox("Active user", USERS, index=USERS.index(st.session_state.selected_user))
        st.caption("Messages sent will be attributed to this user.")

        st.header("Tasklist")

        
        st.divider()
        st.header("Agent")

        # slider temperature
        temp = st.slider("Model temperature", min_value=0.0, max_value=2.0, value=0.0, step=0.1)

        # button for agent creation
        if st.button("(re)Create Agent"):
            llm = build_llm(temperature=temp)
            st.session_state.agent = build_agent(llm)
            st.success("Agent ready.")

    # Chat area
    st.subheader("Conversation (shared between users)")
    for msg in st.session_state.messages["messages"]:
        if isinstance(msg, SystemMessage):
            continue
        author = msg.name if isinstance(msg, HumanMessage) else "assistant"
        if msg.content.rstrip():
            with st.chat_message("user" if isinstance(msg, HumanMessage) else "assistant"):
                st.markdown(msg.content)

    if prompt := st.chat_input(f"{st.session_state.selected_user} diz: "):
        st.session_state.messages["messages"].append(HumanMessage(content="**" + st.session_state.selected_user + "**: " + prompt, name=st.session_state.selected_user))
        with st.chat_message("user"):
            st.markdown(f"**{st.session_state.selected_user}**: {prompt}")

        if st.session_state.agent is None:
            with st.chat_message("assistant"):
                st.warning("Create the agent in the sidebar before asking questions.")
        else:
            with st.spinner("Thinking...", show_time=True) as spinner:
                result = st.session_state.agent.invoke(st.session_state.messages)
                content = result["messages"][-1].content
            if content.rstrip(): 
                with st.chat_message("assistant"):
                    st.markdown(content)
                    st.session_state.messages["messages"].append(AIMessage(content=content))

if __name__ == "__main__":
    main()
