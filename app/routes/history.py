from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from pydantic import BaseModel
from enum import Enum as PyEnum
from app.db import get_db
from app.models.token import chat_history

# Pydantic Enum for the "key" field
class KeyEnum(PyEnum):
    User = "User"
    Ai = "Ai"

# Pydantic model for chat history data
class ChatHistoryCreate(BaseModel):
    user_id: int
    key: KeyEnum
    message: str
    session_id: int

router = APIRouter()

@router.post("/chat_history/")
async def create_chat_history(data: dict, db: AsyncSession = Depends(get_db)):
    query = chat_history.insert().values(
        fingerprint_id=data['fingerprint_id'],
        key=data['key'],  # This should pass the string, not the Enum class
        message=data['message'],
        session_id=data['session_id']
    )
    await db.execute(query)
    await db.commit()
    return {"message": "Chat history inserted successfully"}
