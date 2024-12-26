from dotenv import load_dotenv
from enum import StrEnum
import os


load_dotenv()


class ChannelSetting(StrEnum):
    secret = os.getenv("CHANNEL_SECRET")
    access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    if secret is None or access_token is None:
        raise ValueError("Please set environment variables: CHANNEL_SECRET, CHANNEL_ACCESS_TOKEN")
