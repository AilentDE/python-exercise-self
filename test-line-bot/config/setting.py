from dotenv import load_dotenv
from enum import StrEnum
import os

load_dotenv()


class LineMessageSetting(StrEnum):
    cid = os.getenv("LINE_MESSAGE_CHANNEL_ID")
    secret = os.getenv("LINE_MESSAGE_CHANNEL_SECRET")
    access_token = os.getenv("LINE_MESSAGE_CHANNEL_ACCESS_TOKEN")
    if secret is None or access_token is None:
        raise ValueError(
            "Please set environment variables: LINE_MESSAGE_CHANNEL_SECRET, LINE_MESSAGE_CHANNEL_ACCESS_TOKEN"
        )


class DatabaseSetting(StrEnum):
    host = os.getenv("DATABASE_HOST")
