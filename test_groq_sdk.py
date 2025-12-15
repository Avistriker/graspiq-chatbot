# test_groq_sdk.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

# Test with responses.create (new method)
print("Testing with responses.create method...")
try:
    response = client.responses.create(
        input="Explain the importance of fast language models",
        model="llama-3.1-8b-instant",
        max_completion_tokens=100,
    )
    print("Success!")
    print("Response:", response.output_text)
except Exception as e:
    print(f"Error with responses.create: {e}")

# Test with chat.completions.create (traditional method)
print("\n\nTesting with chat.completions.create method...")
try:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Explain the importance of fast language models"}
        ],
        model="llama-3.1-8b-instant",
        max_tokens=100,
    )
    print("Success!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print(f"Error with chat.completions.create: {e}")