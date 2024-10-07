from sqlalchemy import Table, Column, Integer, String, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from app.db import metadata

tokens = Table(
    "tokens",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fcm_token", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint("fcm_token", name="uq_fcm_token")  # Ensures unique tokens
)