import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    import streamlit as st
    st.error("GEMINI_API_KEY が見つかりません。.env ファイルに GEMINI_API_KEY=your_key を設定してください。")
    st.stop()

genai.configure(api_key=api_key)
MODEL_NAME = "gemini-2.5-flash"


def generate(prompt: str, temperature: float = 0.7) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(temperature=temperature),
    )
    return response.text
