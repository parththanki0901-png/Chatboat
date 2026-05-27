import streamlit as st
import requests
import uuid

st.set_page_config(
    page_title="Chatbot",
    layout="wide"
)

st.title("chatbot")
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "session_id" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.session_id = session_id
    st.session_state.chats[session_id] = []

with st.sidebar:
    st.title("Chats")
    if st.button("New Chat"):
        session_id = str(uuid.uuid4())
        st.session_state.session_id = session_id
        st.session_state.chats[session_id] = []
    st.divider()

    for chat_id, messages in st.session_state.chats.items():
        if len(messages) > 0:
            title = messages[0]["content"][:20]
        else:
            title = "New Chat"
        if st.button(title, key=chat_id):
            st.session_state.session_id = chat_id

messages = st.session_state.chats[st.session_state.session_id]

st.write("current chat")

for msg in messages:
    if msg["role"] == "user":
        st.write(f"you: {msg['content']}")
    else:
        st.write(f"bot: {msg['content']}")

text = st.chat_input("type your message here")

if text:
    messages.append({
        "role": "user",
        "content": text
    })
    with st.chat_message("user"):
        st.write(text)

    data = {
        "message": text,
        "session_id": st.session_state.session_id
    }

    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json=data
        )
        response_data = response.json()


        if "reply" in response_data:

            messages.append({
                "role": "assistant",
                "content": response_data["reply"]
            })
            with st.chat_message("assistant"):
                st.write(response_data["reply"])
        else:
            st.error(
                response_data.get(
                    "detail",
                    "Unknown error"
                )
            )
    except Exception as e:
        st.error(f"Error: {e}")