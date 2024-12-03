# flake8: noqa
from dataclasses import dataclass
from datetime import datetime

from schema.user import UserOutput


@dataclass(slots=False)
class MessageCreate:
    author_id: str
    title: str
    content: str
    permission_level: int = 0


@dataclass(slots=False)
class MessageOutput:
    id: str
    title: str
    createdAt: datetime
    updatedAt: datetime


@dataclass(slots=False)
class MessageOutputCreated(MessageOutput):
    authorId: str
    content: str
    permissionLevel: int


@dataclass(slots=False)
class MessageOutputList(MessageOutput):
    author: UserOutput


@dataclass(slots=False)
class MessageOutputFull(MessageOutputList):
    content: str
    permissionLevel: int
