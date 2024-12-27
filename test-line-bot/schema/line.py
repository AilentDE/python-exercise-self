from pydantic import BaseModel


class LineContentsCreate(BaseModel):
    content_type: str
    content_id: str
