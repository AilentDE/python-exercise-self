from fastapi import APIRouter, Request

from schema.line import LineWebhookEvent
from logic.callback.with_sdk import CallbackLogicSDK
from logic.callback.without_sdk import CallbackLogic

router = APIRouter()


@router.post("/callback")
async def callback(request: Request):

    callback_handler = CallbackLogicSDK()
    await callback_handler.validate_events(request)
    await callback_handler.processing_events()

    return {"result": "ok"}


@router.post("/without_sdk/callback")
async def no_sdk_callback(request: Request, payload: LineWebhookEvent) -> dict:

    callback_handler = CallbackLogic()
    await callback_handler.validate_request(request)
    await callback_handler.processing_events(payload)

    return {"result": "ok"}
