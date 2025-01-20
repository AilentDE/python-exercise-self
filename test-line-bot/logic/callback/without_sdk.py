from fastapi import Request
from fastapi.responses import JSONResponse
from urllib.parse import parse_qs, urlencode, quote
from hashlib import sha1
import requests
import asyncio

from config.setting import LineMessageSetting, LineLoginSetting
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
                print('message', event)
                target = event["source"]["userId"]
                await self.start_loading_animation(target)
                await asyncio.sleep(2)
                await self.reply_message(event["replyToken"], event["message"]["text"])
            elif event["type"] == "postback":
                data = parse_qs(event["postback"]["data"])
                action = data.get('action')
                if action is None:
                    return
                match action[0]:
                    case 'switch':
                        print('switch', data)
                    case 'login':
                        await self.reply_login_url(event["replyToken"], event["source"]["userId"])
                    case 'logout':
                        print('logout', data)
                    case 'register':
                        print('register', data)
                    case _:
                        print('default', data)

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

    def generate_login_url(self, state: str) -> str:
        params = {
            "response_type": "code",
            "client_id": LineLoginSetting.cid,
            "redirect_uri": LineLoginSetting.redirect_uri,
            "state": state,
            "scope": "openid profile",
            "prompt": "consent",
        }

        return f"https://access.line.me/oauth2/v2.1/authorize?{urlencode(params, quote_via=quote)}"

    def flex_btn_message(self, title: str, text: str, btn_text: str, btn_url: str) -> dict:
        return {
            "type": "flex",
            "altText": title,
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "xl"},
                        {"type": "text", "text": text, "wrap": True},
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "style": "primary",
                            "action": {"type": "uri", "label": btn_text, "uri": btn_url},
                        },
                    ],
                },
            },
        }

    async def reply_login_url(self, reply_token: str, user_id: str):
        hashed_user_id = sha1(user_id.encode()).hexdigest()

        url = self.__url + "/message/reply"
        data = {
            "replyToken": reply_token,
            "messages": [
                self.flex_btn_message(
                    title="Login",
                    text="Please login to continue.",
                    btn_text="Login",
                    btn_url=self.generate_login_url(hashed_user_id),
                ),
            ],
        }
        self._session.post(url, json=data)
