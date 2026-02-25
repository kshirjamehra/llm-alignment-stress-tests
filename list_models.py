import os
import asyncio
from dotenv import load_dotenv
from google import genai

load_dotenv()

async def list_models():
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    print("Available Models:")
    models = await client.aio.models.list()
    for m in models:
        print(m.name)

if __name__ == "__main__":
    asyncio.run(list_models())
