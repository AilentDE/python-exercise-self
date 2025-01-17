from fastapi import Request, HTTPException
from linebot.v3.webhook import WebhookParser, WebhookPayload
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import AsyncMessagingApi, ShowLoadingAnimationRequest, ReplyMessageRequest, TextMessage
from linebot.v3.exceptions import InvalidSignatureError
import asyncio

from config.state import line_bot_state


class CallbackLogicSDK:

    _parser: WebhookParser
    _api: AsyncMessagingApi
    events: WebhookPayload | list

    def __init__(self):

        self._parser = line_bot_state.parser
        self._api = line_bot_state.api

    async def validate_events(self, request: Request) -> bool:
        x_line_signature = request.headers.get("X-Line-Signature")
        body = await request.body()

        try:
            self.events = self._parser.parse(body.decode(), x_line_signature)
        except InvalidSignatureError as ex:
            raise HTTPException(status_code=400, detail=str(ex))

    async def processing_events(self):
        for event in self.events:
            if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
                await self.reply_message(event)

    async def reply_message(self, event: MessageEvent):
        await self._api.show_loading_animation(ShowLoadingAnimationRequest(chatId=event.source.user_id, duration=1000))
        await asyncio.sleep(2)
        await self._api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[TextMessage(text=event.message.text)])
        )
