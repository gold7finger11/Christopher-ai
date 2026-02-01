import openai
import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
print("Env var BEFORE dotenv:", os.getenv("XAI_API_KEY") or "Not set")

load_dotenv(override=True)

# ── Connect to xAI Grok API (OpenAI-compatible) ──

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# ── Branding & personality ──
st.set_page_config(page_title="ChristopherAI", page_icon="🤖", layout="wide")
st.title("ChristopherAI")
st.markdown("Your hip, no-BS AI – helpful, direct, witty. Let's go.")

# System prompt – core personality only (fixed and completed)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are Christopher AI — helpful, direct, witty with a hip, chill vibe.
Be concise, smart, and throw in sarcasm or playful roasts when it fits naturally.
Always maximally helpful and truthful. Keep replies sharp and engaging — no fluff, no corporate speak."""
        }
    ]

# Display chat history (skip the system prompt)
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

with st.chat_message("assistant"):
    placeholder = st.empty()
    full_response = ""

    try:
        stream = client.chat.completions.create(
            model="grok-4",
            messages=st.session_state.messages,
            temperature=0.7,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except openai.BadRequestError as e:
        st.error(f"API error: {e}")
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")   
