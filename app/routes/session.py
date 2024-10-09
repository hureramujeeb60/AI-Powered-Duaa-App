from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy import select, insert
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db import AsyncSessionLocal, get_db
from app.models.token import session,chat_history

app = FastAPI()

router = APIRouter()

class SessionCreate(BaseModel):
    fingerprint_id: str


@router.post("/session/")
async def create_session(session_create: SessionCreate, db: AsyncSession = Depends(get_db)):
    # Since user_id is guaranteed to exist, no need to check if user exists.

    # Insert a new session
    query = insert(session).values(fingerprint_id=session_create.fingerprint_id)
    
    await db.execute(query)
    await db.commit()

    # Return success message and user_id
    return {"message": "Session created successfully", "user_id": session_create.fingerprint_id}

@router.get("/sessions/{session_id}/chat-history")
async def get_chat_history(session_id: int, db: AsyncSession = Depends(get_db)):
    # Query chat history for the specified session_id
    query = select(chat_history).where(chat_history.c.session_id == session_id)
    result = await db.execute(query)
    chat_entries = result.fetchall()

    if not chat_entries:
        raise HTTPException(status_code=404, detail="No chat history found for this session")

    # Create a list of dictionaries for each chat entry
    return {"chat_history": [dict(row._mapping) for row in chat_entries]}