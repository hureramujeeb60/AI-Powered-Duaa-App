from fastapi import Request, APIRouter, Depends, FastAPI
from fastapi.responses import StreamingResponse
from app.db import get_db
from app.utils.prompt import SYSTEM_PROMPT
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette.sse import EventSourceResponse
from langchain_together import  ChatTogether
from app.models.token import chat_history  
from enum import Enum as PyEnum


router = APIRouter()

chat = ChatTogether(model="meta-llama/Llama-3-70b-chat-hf", api_key='')

class KeyEnum(PyEnum):
    User = "User"
    Ai = "Ai"

async def insert_chat_history(fingerprint_id: str, key: KeyEnum, message: str, session_id: int, db: AsyncSession):
    query = chat_history.insert().values(
        fingerprint_id=fingerprint_id,
        key=key.value,
        message=message,
        session_id=session_id
    )
    await db.execute(query)
    await db.commit()

@router.get("/dua")
async def dua_endpoint(query: str, fingerprint_id: str, session_id: int, db: AsyncSession = Depends(get_db)):
    async def stream_dua():
        prompt = f"{SYSTEM_PROMPT} Query: {query}"
        accumulated_content = ''

        try:
            stream =  chat.stream(prompt)
            
            for m in stream:
                content = m.content.encode('utf-8').decode('utf-8')
                accumulated_content += content
                print(content)
                yield f"data: {content.strip()}\n\n"
            
            # Print the complete accumulated content after streaming
            print("Complete Response:")
            print(accumulated_content)
            await insert_chat_history(fingerprint_id, KeyEnum.User, query, session_id, db)
            await insert_chat_history(fingerprint_id, KeyEnum.Ai, accumulated_content, session_id, db)
        except Exception as e:
            yield f"data: 'An error occurred: {str(e)}'\n\n"


    return EventSourceResponse(stream_dua(), media_type="text/event-stream")