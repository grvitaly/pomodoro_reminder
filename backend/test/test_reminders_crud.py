import httpx
import json

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

from models.reminders import Reminder
import random


def get_the_token(username: str = "a@b.c", password: str = "p"):
    response = httpx.post(
        "http://localhost:8000/api/token",
        data={"username": username, "password": "p", "grant_type": "password"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    response_json = response.json()
    assert response_json["access_token"] != None
    assert response_json["access_token"] != ""
    assert response_json["token_type"] == "bearer"

    response = httpx.get(
        "http://localhost:8000/api/users/me",
        headers={
            "accept": "application/json",
            "Authorization": "Bearer " + response_json["access_token"],
        },
    )

    assert response.status_code == 200
    resp_json = json.load(response)
    assert resp_json["email"] == "a@b.c"

    return {
        "token": f"Bearer {response_json['access_token']}",
        "user_id": resp_json["id"],
    }


def test_not_authenticated_user_get_reminders():
    response = httpx.get("http://localhost:8000/api/reminders")
    assert response.status_code == 307


def test_not_authenticated_user_create_reminder():
    response = httpx.post("http://localhost:8000/api/reminders")
    assert response.status_code == 307


def test_not_authenticated_user_update_reminder():
    response = httpx.put("http://localhost:8000/api/reminders")
    assert response.status_code == 307


def test_not_authenticated_user_delete_reminder():
    response = httpx.delete("http://localhost:8000/api/reminders")
    assert response.status_code == 307


def create_headers(token):
    return {
        "accept": "application/json",
        "Authorization": token,
        "Content-Type": "application/json",
    }


def test_create_reminder():
    resp = get_the_token()

    reminder_json = {
        "date_created": "2023-07-14T22:00:27.227Z",
        "date_last_updated": "2023-07-14T22:00:27.227Z",
        "owner_id": resp["user_id"],
        "is_music_on": False,
        "is_music_shuffle": False,
        "current_music_list_id": 0,
        "music_list_song_number": 0,
        "position_within_song": 0,
    }

    response = httpx.post(
        "http://localhost:8000/api/reminders/",
        json=reminder_json,
        headers=create_headers(resp["token"]),
    )

    assert response.status_code == 200


def get_reminders_list():
    resp = get_the_token()
    response = httpx.get(
        "http://localhost:8000/api/reminders/", headers=create_headers(resp["token"])
    )

    assert response.status_code == 200
    return {"reminders": response.json(), "token": resp}


def test_get_reminders_list():
    list_of_reminders = get_reminders_list()
    assert len(list_of_reminders["reminders"]) > 0


def test_get_reminder():
    list_of_reminders = get_reminders_list()
    random_reminder = random.choice(list_of_reminders["reminders"])
    response = httpx.get(
        f"http://localhost:8000/api/reminders/{random_reminder['id']}",
        headers=create_headers(list_of_reminders["token"]["token"]),
    )

    assert response.status_code == 200
    resp_json = json.load(response)
    assert resp_json["owner_id"] == list_of_reminders["token"]["user_id"]


def test_update_reminder():
    list_of_reminders = get_reminders_list()
    random_reminder = random.choice(list_of_reminders["reminders"])
    data = {
        "id": random_reminder["id"],
        "owner_id": list_of_reminders["token"]["user_id"],
        "is_music_on": "true",
        "is_music_shuffle": "true",
        "current_music_list_id": "0",
        "music_list_song_number": "23",
        "position_within_song": "221",
        "date_created": "2023-07-15T00:45:26.951Z",
        "date_last_updated": "2023-07-15T00:45:26.951Z",
    }
    response = httpx.put(
        f"http://localhost:8000/api/reminders/",
        json=data,
        headers=create_headers(list_of_reminders["token"]["token"]),
    )

    assert response.status_code == 200


def test_delete_reminder():
    list_of_reminders = get_reminders_list()
    random_reminder = random.choice(list_of_reminders["reminders"])

    response = httpx.delete(
        f"http://localhost:8000/api/reminders/{random_reminder['id']}",
        headers=create_headers(list_of_reminders["token"]["token"]),
    )

    assert response.status_code == 204
