from robyn import Robyn, logger, Request

from routes.user import router as user_router
from routes.subscribe import router as subscribe_router
from routes.message import router as message_router
from routes.history import router as history_router

from config.database import create_all
from utils.db_base import create_base_premission

app = Robyn(__file__)
app.include_router(user_router)
app.include_router(subscribe_router)
app.include_router(message_router)
app.include_router(history_router)


@app.startup_handler
async def on_startup():
    await create_all()
    await create_base_premission()


@app.get("/")
async def h(request: Request):
    return "Hello, world!"


@app.get("/test_log")
async def test_log(request: Request):
    logger.info("This is an info message")
    logger.warn("This is a warning message")
    logger.error("This is an error message")
    return "Check the logs"


app.start()
# start by: python -m robyn app.py --dev
