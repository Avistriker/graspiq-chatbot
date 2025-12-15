# test_sambanova.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("SAMBA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

print("Testing SambaNova API with DeepSeek-V3.1-Terminus model...")

try:
    response = client.chat.completions.create(
        model="DeepSeek-V3.1-Terminus",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"}
        ],
        temperature=0.1,
        top_p=0.1,
        max_tokens=100
    )
    
    print("✅ SambaNova API is working!")
    print(f"Response: {response.choices[0].message.content}")
    print(f"Model: {response.model}")
    print(f"Finish reason: {response.choices[0].finish_reason}")
    
    # Test with a placement-related question
    print("\n\nTesting with placement question...")
    response2 = client.chat.completions.create(
        model="DeepSeek-V3.1-Terminus",
        messages=[
            {"role": "system", "content": "You are a career placement advisor."},
            {"role": "user", "content": "How to prepare for technical interviews?"}
        ],
        temperature=0.1,
        top_p=0.1,
        max_tokens=200
    )
    
    print(f"Response: {response2.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if your API key is correct (without < > brackets)")
    print("2. Make sure you have internet connectivity")
    print("3. Verify SambaNova API is available")
    print("4. Check if you have API credits/access")