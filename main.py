import streamlit as st
from llm_chains import load_normal_chain
from langchain.memory import StreamlitChatMessageHistory

def load_chain(chat_history):
    return load_normal_chain(chat_history) 

def clear_input():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def set_send_input():
    st.session_state.send_input = True
    clear_input()

def main():
    st.title('Mock SAGA Chatbot')
    chat_container = st.container()

    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""

    chat_history = StreamlitChatMessageHistory(key="history")
    llm_chain = load_chain(chat_history)

    user_input = st.text_input("User Input", key="user_input", on_change=set_send_input)

    send_button = st.button("Send", key="send_button")

    if send_button or st.session_state.send_input:      

        if st.session_state.user_question != "":
            
            with chat_container:
                llm_response = llm_chain.run(st.session_state.user_question)
                st.session_state.user_question = ""
        
        if chat_history.messages != []:
            with chat_container:
                st.write("Chat History")
                for message in chat_history.messages:
                    st.chat_message(message.type).write(message.content)

if __name__ == "__main__":
    main()