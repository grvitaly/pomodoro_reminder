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

import pytest
import random
import string

import httpx
import json


def random_char(char_num):
    email = "".join(random.choice(string.ascii_lowercase) for _ in range(char_num))
    email = email + "@gmail.com"
    return email


def test_user_create():
    email = random_char(10)

    user_json = {
        "date_created": "2023-07-14T02:52:40.005Z",
        "date_last_updated": "2023-07-14T02:52:40.005Z",
        "email": email,
        "hashed_password": "pass",
        "is_active": "true",
        "user_role": 1,
    }
    response = httpx.post("http://localhost:8000/api/users", json=user_json)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["access_token"] != None
    assert response_json["access_token"] != ""
    assert response_json["token_type"] == "bearer"


def test_user_generate_token():
    response = httpx.post(
        "http://localhost:8000/api/token",
        data={"username": "a@b.c", "password": "p", "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["access_token"] != None
    assert response_json["access_token"] != ""
    assert response_json["token_type"] == "bearer"


def test_user_get_current_user():
    pass
