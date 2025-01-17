from fastapi import Request
from fastapi.responses import JSONResponse
import requests
import asyncio

from config.setting import LineMessageSetting
from schema.line import LineWebhookEvent
from utils.validator import check_signature


class CallbackLogic:

    __url: str = "https://api.line.me/v2/bot"
    _token: str
    _session: requests.Session

    def __init__(self):
        self._token = LineMessageSetting.access_token
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {self._token}",
            }
        )

    async def validate_request(self, request: Request):
        body = await request.body()
        decoded_body = body.decode()

        if not check_signature(decoded_body, request.headers.get("X-Line-Signature")):
            return JSONResponse(status_code=400, content={"message": "Invalid signature"})

    async def processing_events(self, event_payload: LineWebhookEvent):
        for event in event_payload.events:
            if event["type"] == "message" and event["message"]["type"] == "text":
                target = event["source"]["userId"]
                await self.start_loading_animation(target)
                await asyncio.sleep(2)
                await self.reply_message(event["replyToken"], event["message"]["text"])

    async def start_loading_animation(self, chat_id: str, delay: int = 10):
        url = self.__url + "/chat/loading/start"
        data = {"chatId": chat_id, "loadingSeconds": delay}
        self._session.post(url, json=data)

    async def reply_message(self, reply_token: str, msg: str):
        url = self.__url + "/message/reply"
        data = {
            "replyToken": reply_token,
            "messages": [
                {"type": "text", "text": msg},
            ],
        }
        self._session.post(url, json=data)
