from pydantic import BaseModel
from datetime import datetime


class LogSchema(BaseModel):
    type: str
    message: str
    created_at: datetime | None = None
