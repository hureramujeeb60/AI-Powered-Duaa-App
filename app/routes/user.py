from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy import select, insert
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db import AsyncSessionLocal, get_db
from app.models.token import users

app = FastAPI()

router = APIRouter()

class UserCreate(BaseModel):
    user_id: int

async def get_user_by_user_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(users).where(users.c.user_id == user_id))
    return result.scalar_one_or_none()

@router.post("/api/users/")
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_db)):
    # Check if the user already exists
    result = await session.execute(select(users).where(users.c.user_id == user_create.user_id))
    existing_user = result.scalar_one_or_none()

    # If user exists, do nothing
    if existing_user:
        return {"message": "User already exists", "user_id": user_create.user_id}

    # If user does not exist, insert new user
    new_user = insert(users).values(user_id=user_create.user_id)
    await session.execute(new_user)
    await session.commit()

    return {"message": "User created", "user_id": user_create.user_id}