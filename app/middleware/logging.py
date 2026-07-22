import time
from fastapi import FastAPI, Request
app = FastAPI()
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = f"{duration:.4f} sec"
    response.headers["X-App-Name"] = "Ticket Management API"
    response.headers["X-Version"] = "1.0.0"
    return response