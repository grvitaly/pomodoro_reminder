import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from database import engine
import pytest
from models.users import User
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session


def test_database_connection_parameters():
    session = Session(engine)
    users = session.query(User).first()
    assert users != None


def test_insert_duplicate_email():
    session = Session(engine)
    user = User(email="a@b.c", hashed_password="p")
    user.encrypt_password()
    with pytest.raises(IntegrityError):
        session.add(user)
        session.commit()
