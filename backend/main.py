from fastapi import FastAPI
from crud.users import router as users_router
from crud.reminders import router as reminders_router
from sqlmodel import SQLModel
from database import engine
import uvicorn

app = FastAPI()
app.include_router(users_router)
app.include_router(reminders_router)


@app.post("/api/init_database")
async def init_database():
    SQLModel.metadata.create_all(engine)
    return {"message": "Database created"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
