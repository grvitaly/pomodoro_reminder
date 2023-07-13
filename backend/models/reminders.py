from datetime import datetime
from sqlmodel import SQLModel, Field, DateTime
from typing import Optional
from models.base import BaseID, OwnerID, Timestamps


class Reminder(BaseID, OwnerID, Timestamps, table=True):
    is_music_on: bool = Field(default=False)
    is_music_shuffle: bool = Field(default=False)
    current_music_list_id: Optional[int]
    music_list_song_number: Optional[int]
    position_within_song: Optional[int]


class ToDoTask(BaseID, OwnerID, Timestamps, table=True):
    parent_task_id: Optional[int]
    task_title: str
    task_description: str
    percent_complete: int


class LocationReminder(BaseID, OwnerID, Timestamps, table=True):
    is_music_on: bool = Field(default=False)
    is_music_shuffle: bool = Field(default=False)
    current_music_list_id: Optional[int]
    music_list_song_number: Optional[int]
    position_within_song: Optional[int]
