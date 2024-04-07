import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRES_CONN_STRING")
    APP_VERSION = os.environ.get("APP_VERSION")

config = Config()