import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    SUBSCRIBE_INTERVAL_MINUTES = int(os.getenv("SUBSCRIBE_INTERVAL_MINUTES"))
    API_TOKEN = os.getenv("API_TOKEN")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_HOST = os.getenv("API_HOST")
    API_PORT = int(os.getenv("API_PORT"))
