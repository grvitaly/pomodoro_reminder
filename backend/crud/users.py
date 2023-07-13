from models.users import User

import jwt as _jwt

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from database import engine


oauth2schema = OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"


def get_session():
    with Session(engine) as session:
        yield session


async def get_user_by_email(email: str, session: Session):
    return session.query(User).filter(User.email == email).first()


async def create_token(user: User):
    user_dict = dict(id=user.id, email=user.email)
    access_token = _jwt.encode(user_dict, JWT_SECRET, algorithm="HS256")
    return dict(
        access_token=access_token,
        token_type="bearer",
    )


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = session.query(User).get(payload["id"])
    except:
        raise HTTPException(status_code=401, detail="Invalid user or password")

    return user


router = APIRouter(prefix="/api")


@router.post("/users")
async def create_user(user: User, session: Session = Depends(get_session)):
    db_user = await get_user_by_email(user.email, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")

    user.encrypt_password()
    session.add(user)
    session.commit()
    session.refresh(user)

    return await create_token(user)


@router.post("/token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = await get_user_by_email(form_data.username, session)

    if not user:
        raise HTTPException(
            status_code=401, detail=f"No such user ${form_data.username}"
        )

    if not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=401, detail=f"Invalid Credentials for ${form_data.username}"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=401, detail=f"User ${form_data.username} deactivated"
        )

    return await create_token(user)


@router.get("/api/users/me", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user
