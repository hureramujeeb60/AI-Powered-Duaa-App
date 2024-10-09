from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy import select, insert
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db import AsyncSessionLocal, get_db
from app.models.token import session

app = FastAPI()

router = APIRouter()

class SessionCreate(BaseModel):
    user_id: int


@router.post("/api/session/")
async def create_session(session_create: SessionCreate, db: AsyncSession = Depends(get_db)):
    # Since user_id is guaranteed to exist, no need to check if user exists.

    # Insert a new session
    query = insert(session).values(usr_id=session_create.user_id)
    
    await db.execute(query)
    await db.commit()

    # Return success message and user_id
    return {"message": "Session created successfully", "user_id": session_create.user_id}