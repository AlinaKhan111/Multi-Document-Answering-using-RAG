import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_with_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-flash-latest")

    try:
        response = model.generate_content(prompt)
        return response.text

    except ResourceExhausted:
        return (
            "⚠️ LLM API quota exceeded.\n\n"
            "Please wait and try again later."
        )
