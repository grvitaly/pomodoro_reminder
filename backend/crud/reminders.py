from fastapi import Depends, HTTPException, APIRouter
from datetime import datetime
from typing import List

from crud.users import get_session, get_current_user
from models.users import User
from models.reminders import Reminder
from sqlmodel import Session


def reminder_selector(reminder_id: int, session: Session) -> Reminder:
    reminder = session.get(Reminder, reminder_id)
    if reminder is None:
        raise HTTPException(status_code=404, detail="Lead does not exist")
    return reminder


router = APIRouter(prefix="/api/reminders")


@router.post("/", response_model=Reminder)
async def create_reminder(
    reminder: Reminder,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    reminder.owner_id = user.id
    session.add(reminder)
    session.commit()
    session.refresh(reminder)
    return reminder


@router.get("/", response_model=List[Reminder])
async def get_leads(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    list = session.query(Reminder).filter_by(owner_id=user.id)
    if list.count() == 0:
        raise HTTPException(status_code=401, detail="You don't have any reminders")
    return list


@router.get("/{reminder_id}", status_code=200)
async def get_reminder(
    reminder_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return reminder_selector(reminder_id=reminder_id, session=session)


@router.delete("/{reminder_id}", status_code=204, description="Successfully deleted")
async def delete_reminder(
    reminder_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    reminder = reminder_selector(reminder_id=reminder_id, session=session)
    session.delete(reminder)
    session.commit()


@router.put("/", status_code=200, description="Successfully updated")
async def update_reminder(
    updated_reminder: Reminder,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    rs = reminder_selector(reminder_id=updated_reminder.id, session=session)
    reminder_dict = rs.dict(
        exclude_unset=True, exclude={"date_created", "date_last_updated"}
    )
    for key, value in reminder_dict.items():
        setattr(rs, key, value)

    rs.owner_id = user.id
    rs.date_last_updated = datetime.utcnow

    session.add(rs)
    session.commit()
    session.refresh()

    return rs
