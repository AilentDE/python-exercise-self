from fastapi import APIRouter

from logic.rich_menu import RichMenuLogic, SampleRichMenu

router = APIRouter()


@router.get("/list")
async def get_rich_menu_list():
    rich_menus = RichMenuLogic().get_richmenu_list()
    return {"result": rich_menus}


@router.get("/alias")
async def get_rich_menu_alias():
    rich_menus = RichMenuLogic().get_richmenu_alias()
    return {"result": rich_menus}


@router.post("/init")
async def initialize_rich_menu():
    handler = SampleRichMenu()
    handler.clear_assets()
    handler.create_sample_richmenu()
    return {"result": "ok"}
