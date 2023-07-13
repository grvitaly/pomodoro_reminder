from sqlmodel import create_engine
from sqlalchemy.engine.url import URL
import os
from dotenv import load_dotenv

load_dotenv()

url_object = URL.create(
    drivername=os.getenv("DRIVER_NAME"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    database=os.getenv("DATABASE"),
)

engine = create_engine(url_object, echo=True)
