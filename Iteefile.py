from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
import streamlit as st
st.set_page_config(page_title="Prompt Enhancer", page_icon="📝")
st.title("📝 Prompt Engineer — General Prompt Enhancer")


st.caption("Demo Mode - Learn how to structure better prompts!")


st.subheader("Enter Role, Context, Task (RCT)")
role = st.text_input("Role", value="a helpful assistant")
context = st.text_area("Context", value="Audience: busy professional; Goal: clear and specific")
task = st.text_area("Task", value="Rewrite my draft for clarity and ask 1 clarifying question")


st.subheader("Paste your rough prompt")


draft = st.text_area("Your draft prompt:", height=140)


if st.button("Enhance Prompt"):
   if not draft.strip():
       st.error("Please enter a valid draft prompt before enhancing.")

