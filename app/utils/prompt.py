from langchain_together import ChatTogether
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

chat = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", api_key='TOGETHER_API_KEY')

SYSTEM_PROMPT = """
You are an Islamic scholar providing Duas based on the user's query. 
If the user asks for a valid Dua query (like "Dua for anger" or "anger"), respond with:
1. The Arabic text of the Dua.
2. The English translation of the Dua.
3. The reference (e.g., Sahih Bukhari) for the Dua.

If the user's query does not contain a valid Dua request or intention, return the following message:
"I'm sorry, your query does not relate to a specific Islamic Dua. Please provide a valid request like 'Dua for anger'."
"""

async def stream_dua(query: str):
    prompt = f"{SYSTEM_PROMPT} Query: {query}"
    
    dua_content = ""
    
    for m in chat.stream(prompt):
        content = m.content.encode('utf-8').decode('utf-8')
        dua_content += content

    yield f"data: {dua_content.strip()}\n\n"

async def get_dua_for_prayer(prayer_name: str) -> str:
    query = f"Dua for {prayer_name} prayer"
    dua_stream = stream_dua(query)
    dua = ""
    async for chunk in dua_stream:
        dua += chunk
    return dua

# if __name__ == "__main__":
#     prayer_name = "Dhuhr"
#     dua = asyncio.run(get_dua_for_prayer(prayer_name))
#     print(dua)
