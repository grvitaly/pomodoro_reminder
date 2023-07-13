from passlib.hash import bcrypt
from sqlmodel import SQLModel, Field
from typing import Optional
from models.base import BaseID, Timestamps


class User(BaseID, Timestamps, table=True):
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    user_role: int = Field(default=1)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

    def encrypt_password(self):
        self.hashed_password = bcrypt.hash(self.hashed_password)
