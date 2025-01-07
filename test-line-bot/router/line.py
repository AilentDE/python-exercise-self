from fastapi import APIRouter, Request, HTTPException, Header
from linebot.v3.messaging import ReplyMessageRequest, TextMessage, ShowLoadingAnimationRequest
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
import json
from pprint import pprint
import asyncio

from config.state import line_bot_state
from schema.line import LineWebhookEvent
from utils.validator import check_signature
from utils.webhook_reply import WebhookReplay

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


@router.post("/without_sdk/callback")
async def no_sdk_callback(request: Request, payload: LineWebhookEvent, x_line_signature: str = Header()) -> dict:
    """Line callback.

    Args:
        request (Request): The request object containing the callback data.
        payload (LineWebhookEvent): The payload.

    Returns:
        dict: The response body.

    # Raises:
    #     ex: The exception that occurred.
    """
    body = await request.body()
    decoded_body = body.decode("utf-8")

    if not x_line_signature or not check_signature(decoded_body, x_line_signature):
        return {"status": "error"}

    for event in payload.events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            reply_handler = WebhookReplay(chat_id=event["source"]["userId"])
            reply_handler.start_loading_animation()
            await asyncio.sleep(5)
            reply_handler.reply_text(event["replyToken"], event["message"]["text"])
    return {"status": "ok"}
