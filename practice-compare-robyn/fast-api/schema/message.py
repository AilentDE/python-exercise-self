from datetime import datetime
from pydantic import BaseModel

from schema.base import CamelSchema
from schema.user import User


class MessageCreate(BaseModel):
    title: str
    content: str
    permission_level: int = 0


class MessageCreated(MessageCreate, CamelSchema):
    id: str
    author_id: str
    created_at: str
    updated_at: str


class Message(CamelSchema):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageWithAuthor(Message):
    author: User


class MessageFull(MessageWithAuthor):
    content: str
    permission_level: int
