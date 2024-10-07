# from fastapi import APIRouter, HTTPException, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select
# # from app.models.token import tokens
# from app.db import AsyncSessionLocal, get_db


# router = APIRouter()


# @router.post("/register")
# async def register_user(email: str, device_token: str, db: AsyncSession = Depends(get_db)):
#     result = await db.execute(select(tokens).where(tokens.email == email))
#     existing_user = result.scalars().first()
    
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already registered.")

#     new_user = tokens(email=email, device_token=device_token)
#     db.add(new_user)
#     await db.commit()
#     await db.refresh(new_user)

#     return {"message": "User registered successfully.", "user_id": new_user.id}