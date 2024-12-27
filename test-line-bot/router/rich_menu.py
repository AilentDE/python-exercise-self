from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from requests import Session, RequestException

# from config.setting import ChannelSetting
from config.database import get_session
from schema.line import LineContentsCreate
from utils.sample_body import fake_rich_menu
from utils.db_handler import insert_data, fetch_data_one, delete_data_one
from utils.line_session_handler import get_line_session

router = APIRouter()


@router.post("/create")
async def create_rich_menu(line_session: Session = Depends(get_line_session), db_session: AsyncSession = Depends(get_session)):
    url = "https://api.line.me/v2/bot/richmenu"

    try:
        r = line_session.post(url, json=fake_rich_menu)
        r.raise_for_status()
    except RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    await insert_data(db_session, LineContentsCreate(
        content_type="rich_menu",
        content_id=r.json()["richMenuId"],
    ))

    return {"result": "ok"}


@router.post("/upload_image")
async def upload_image(line_session: Session = Depends(get_line_session), db_session: AsyncSession = Depends(get_session)):
    current_rich_menu = await fetch_data_one(db_session, "rich_menu")
    if not current_rich_menu:
        raise HTTPException(status_code=404, detail="rich_menu not found")

    with open("assets/richmenu-template-guide-04.png", "rb") as f:
        url = f"https://api-data.line.me/v2/bot/richmenu/{current_rich_menu.content_id}/content"
        line_session.headers.update({
            "Content-Type": "image/png"
        })
        try:
            r = line_session.post(url, data=f)
            r.raise_for_status()
        except RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"result": "ok"}


@router.post("/set_default")
async def set_default_rich_menu(line_session: Session = Depends(get_line_session), db_session: AsyncSession = Depends(get_session)):
    current_rich_menu = await fetch_data_one(db_session, "rich_menu")
    if not current_rich_menu:
        raise HTTPException(status_code=404, detail="rich_menu not found")

    url = f"https://api.line.me/v2/bot/user/all/richmenu/{current_rich_menu.content_id}"
    try:
        r = line_session.post(url)
        r.raise_for_status()
    except RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": "ok"}


@router.delete("/unset_default")
async def clear_default_rich_menu(line_session: Session = Depends(get_line_session)):
    url = "https://api.line.me/v2/bot/user/all/richmenu"
    try:
        r = line_session.delete(url)
        r.raise_for_status()
    except RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"result": "ok"}


@router.delete("/delete")
async def delete_rich_menu(line_session: Session = Depends(get_line_session), db_session: AsyncSession = Depends(get_session)):
    current_rich_menu = await fetch_data_one(db_session, "rich_menu")
    if not current_rich_menu:
        raise HTTPException(status_code=404, detail="rich_menu not found")

    url = f"https://api.line.me/v2/bot/richmenu/{current_rich_menu.content_id}"
    try:
        r = line_session.delete(url)
        r.raise_for_status()
    except RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    await delete_data_one(db_session, current_rich_menu.content_id)
    return {"result": "ok"}
