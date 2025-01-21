from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys

from config.state import line_bot_state
from config.database import create_all
from config.setting import LineLoginSetting

from router.line import router as line_router
from router.rich_menu import router as rich_menu_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("|| server startup")
    line_bot_state.generate_api()
    await create_all()
    yield
    print("|| server shutdown")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[LineLoginSetting.redirect_uri[:-1]],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(line_router, prefix="/line", tags=["line"])
app.include_router(rich_menu_router, prefix="/rich_menu", tags=["rich_menu"])


@app.get("/")
async def root():
    return {"Python": sys.version}
