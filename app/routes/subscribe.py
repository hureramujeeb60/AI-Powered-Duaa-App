from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update
from app.db import get_db
from app.models import token  # Assuming tokens is your tokens model

router = APIRouter()

# API to subscribe/save FCM token
@router.post("/subscribe")
async def subscribe_to_notifications(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    fcm_token = data.get('fcm_token')

    # Validate the input
    if not fcm_token:
        raise HTTPException(status_code=400, detail="FCM token is required")

    try:
        # Insert the FCM token if it doesn't exist, or update if it already exists
        stmt = insert(token).values(fcm_token=fcm_token).on_conflict_do_nothing()
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving FCM token: {str(e)}")

    return {"message": "Successfully subscribed to notifications"}

# Unsubscribe endpoint to remove the FCM token
@router.post("/unsubscribe")
async def unsubscribe_from_notifications(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    fcm_token = data.get('fcm_token')

    if not fcm_token:
        raise HTTPException(status_code=400, detail="FCM token is required")

    try:
        # Remove the token from the database
        stmt = token.delete().where(token.c.fcm_token == fcm_token)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error unsubscribing: {str(e)}")

    return {"message": "Successfully unsubscribed from notifications"}
