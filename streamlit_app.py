import streamlit as st
from openai import OpenAI

# Access the OpenAI API key from the secrets
api_key = st.secrets["OPENAI_API_KEY"]