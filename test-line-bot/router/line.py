from fastapi import APIRouter, Request, HTTPException
from linebot.v3.messaging import ReplyMessageRequest, TextMessage, ShowLoadingAnimationRequest
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import json
from pprint import pprint
import asyncio

from config.state import line_bot_state

router = APIRouter()


@router.post("/callback")
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature")
    body = await request.body()
    pprint(json.loads(body.decode()))

    try:
        events = line_bot_state.parser.parse(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            await line_bot_state.api.show_loading_animation(
                ShowLoadingAnimationRequest(chatId=event.source.user_id, duration=1000)
            )
            await asyncio.sleep(2)
            await line_bot_state.api.reply_message(
                ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)])
            )
    return {"result": "ok"}
