from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy import select, insert
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db import AsyncSessionLocal, get_db
from app.models.token import users, session

app = FastAPI()

router = APIRouter()

class UserCreate(BaseModel):
    fingerprint: str

async def get_user_by_user_id(fingerprint_id: str, db: AsyncSession):
    result = await db.execute(select(users).where(users.c.fingerprint == fingerprint_id))
    return result.scalar_one_or_none()

@router.post("/users/")
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_db)):
    # Check if the user already exists
    result = await session.execute(select(users).where(users.c.fingerprint == user_create.fingerprint))
    existing_user = result.scalar_one_or_none()

    # If user exists, do nothing
    if existing_user:
        return {"message": "User already exists", "user_id": user_create.fingerprint}

    # If user does not exist, insert new user
    new_user = insert(users).values(fingerprint=user_create.fingerprint)
    await session.execute(new_user)
    await session.commit()

    return {"message": "User created", "user_id": user_create.fingerprint}

@router.get("/users/{fingerprint}/sessions")
async def get_user_sessions(fingerprint: str, db: AsyncSession = Depends(get_db)):
    # Check if the user exists
    query = select(users).where(users.c.fingerprint == fingerprint)
    result = await db.execute(query)
    user = result.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Query sessions of the user
    sessions_query = select(session).where(session.c.fingerprint_id == fingerprint)
    sessions_result = await db.execute(sessions_query)
    sessions = sessions_result.fetchall()

    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this user")
    
    # Return the list of sessions
    return {"sessions": [dict(row._mapping) for row in sessions]}