import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print("Using API Key:", api_key)

client = OpenAI(api_key=api_key)

try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ],
        temperature=0.7,
        max_tokens=100
    )
    print("Response choice content:", response.choices[0].message.content)
except Exception as e:
    print("Error details:", type(e), e)
