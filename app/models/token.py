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
    Column("fingerprint", String, nullable=False),
    UniqueConstraint("fingerprint", name="uq_fingerprint"),  # Optional if needed
)

session = Table(
    "session",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fingerprint_id", String, ForeignKey("users.fingerprint", ondelete="CASCADE"), nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now())
)

chat_history = Table(
    "chat_history",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fingerprint_id", String, ForeignKey("users.fingerprint"), nullable=False),
    Column("key", Enum("User", "Ai", name="key_enum"), nullable=False),
    Column("message", Text, nullable=False),
    Column("session_id", Integer, ForeignKey("session.id", ondelete="CASCADE"), nullable=False),
)
