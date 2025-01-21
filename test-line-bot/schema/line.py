from pydantic import BaseModel


class LineContentsCreate(BaseModel):
    content_type: str
    content_id: str


class LineWebhookEvent(BaseModel):
    """Line Webhook Event Schema

    Attributes:
        destination (str): The destination.
        events (list[dict]): The events.
    """

    destination: str
    events: list[dict]


class LineLoginPayload(BaseModel):
    """Line Auth Code Schema

    Attributes:
        code (str): The code.
    """

    code: str
