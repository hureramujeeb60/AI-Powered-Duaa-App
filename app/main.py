import os
# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import dua, user, session, history
from app.db import init_db, engine, metadata


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(dua.router)
app.include_router(user.router)
app.include_router(session.router)
app.include_router(history.router)
# app.include_router(register.router)
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await init_db()





