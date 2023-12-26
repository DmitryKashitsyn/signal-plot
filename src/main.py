import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.router.router import router


app = FastAPI(
    title="Graph Backend",
    version="dev",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_request_header(request: Request, call_next: callable):
    start_time = time.time()
    response = await call_next(request)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


app.include_router(router)

