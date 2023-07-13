from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, text


class BaseID(SQLModel):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


class OwnerID(SQLModel):
    owner_id: int = Field(nullable=False, index=True)


class Timestamps(SQLModel):
    date_created: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        ),
    )
    date_last_updated: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
            server_onupdate=text("now()"),
        ),
    )
