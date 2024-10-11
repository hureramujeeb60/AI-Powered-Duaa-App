from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
from pydantic import BaseModel
from enum import Enum as PyEnum
from app.db import get_db
from app.models.token import chat_history, session

# Pydantic Enum for the "key" field
class KeyEnum(PyEnum):
    User = "User"
    Ai = "Ai"

# Pydantic model for chat history data
class ChatHistoryCreate(BaseModel):
    fingerprint_id: str
    key: KeyEnum
    message: str
    session_id: int

router = APIRouter()

async def get_first_message_by_session_id(session_id: int, db: AsyncSession):
    """Fetches the first message for a given session_id"""
    result = await db.execute(
        select(chat_history.c.message).where(chat_history.c.session_id == session_id).limit(1)
    )
    return result.scalar()  # scalar() gets the first column of the first row

async def update_session_name(session_id: int, session_name: str, db: AsyncSession):
    """Updates the session name for the given session_id"""
    query = (
        update(chat_history)
        .where(session.c.id == session_id)
        .values(session_name=session_name)
    )
    await db.execute(query)
    await db.commit()

@router.post("/chat_history/")
async def create_chat_history(data: ChatHistoryCreate, db: AsyncSession = Depends(get_db)):

    first_message = await get_first_message_by_session_id(data.session_id, db)

    if not first_message:
        # No chat history for this session, use the current message as the session name
        session_name = data.message
    else:
        # Use the first message from the existing chat history as the session name
        session_name = first_message
    
    query = chat_history.insert().values(
        fingerprint_id=data.fingerprint_id,
        key=data.key.value,
        message=data.message,
        session_id=data.session_id
        # session_name= session_name
    )
    await db.execute(query)
    await db.commit()

    # Update the session name after inserting the message
    await update_session_name(data.session_id, session_name, db)

    return {"message": "Chat history inserted successfully", "session_name": session_name}
