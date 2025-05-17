from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text: str) -> str:
    """Generates a summary of the input text using OpenAI GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize the following:\n{text}"}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content