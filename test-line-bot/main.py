from fastapi import FastAPI
from contextlib import asynccontextmanager

from config.state import line_bot_state
from router.line import router as line_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("|| server startup")
    line_bot_state.generate_api()
    yield
    print("|| server shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(line_router, prefix="/line", tags=["line"])


@app.get("/")
async def root():
    return {"Hello": "World"}
