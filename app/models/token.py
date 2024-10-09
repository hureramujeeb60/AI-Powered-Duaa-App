from sqlalchemy import Table, Column, Integer, String, UniqueConstraint, DateTime, ForeignKey, Enum, Text
from sqlalchemy.sql import func
from app.db import metadata

tokens = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fcm_token", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint("fcm_token", name="uq_fcm_token")
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("user_id", Integer, nullable=False),
    UniqueConstraint("user_id", name="uq_user_id"),  # Optional if needed
)

session = Table(
    "session",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("usr_id", Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

chat_history = Table(
    "chat_history",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("history_user_id", Integer, ForeignKey("user.id"), nullable=False),
    Column("key", Enum("User", "Ai", name="key_enum"), nullable=False),
    Column("message", Text, nullable=False),
    Column("session_id", Integer, ForeignKey("session.id", ondelete="CASCADE"), nullable=False),
)
