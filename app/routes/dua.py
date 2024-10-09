from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from app.utils.prompt import SYSTEM_PROMPT
import asyncio
from sse_starlette.sse import EventSourceResponse
from langchain_together import  ChatTogether


router = APIRouter()

chat = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", api_key='')


@router.get("/dua")
def dua_endpoint(query: str):
    def stream_dua():
        prompt = f"{SYSTEM_PROMPT} Query: {query}"

        try:
            # This should be an async iterable
            stream =  chat.stream(prompt)
            
            for m in stream:  # Await the stream to ensure it is async
                if m.content:  # Check if content exists`
                    print('*****************', m.content)
                    yield f"data: {m.content.strip()}\n\n"
        except Exception as e:
            yield f"data: 'An error occurred: {str(e)}'\n\n"


    return EventSourceResponse(stream_dua())