from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import time


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()  # 紀錄開始時間
        response = await call_next(request)  # 處理請求
        process_time = (time.perf_counter() - start_time) * 1000  # 計算處理時間（毫秒）
        logger.info(f"URL: {request.url.path}, Method: {request.method}, Process Time: {process_time:.2f} ms")
        return response
