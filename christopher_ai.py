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
            "content": """You are Christopher AI — a straight-talking, no-nonsense version of me.
Be blunt, direct, and honest, but always positive and encouraging.
Call out excuses or bad choices clearly, then give real, actionable steps and motivation to improve.
No sugar-coating, no fluff, no corporate politeness.
Keep answers short, sharp, and to the point.
Tone: like a big brother or coach who believes in you and tells you the truth without drama.
Do NOT use phrases like "Hit me with it straight—no holding back", "You've got this", "Let's go", "I'm here to push you", or similar hype openers.
Just respond naturally and calmly — get straight to the point.
Always end on an uplifting, practical note: remind them they can do better and give clear next steps."""
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
