import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

EMAIL = "24f1002646@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-uczmu5.example.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def core_policy_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{duration:.6f}"
    return response

@app.get("/")
def home():
    return {"status": "running"}

@app.get("/stats")
def stats(values: str = Query(...)):
    nums = [int(x.strip()) for x in values.split(",") if x.strip()]
    total_count = len(nums)
    total_sum = sum(nums)
    return {
        "email": EMAIL,
        "count": total_count,
        "sum": total_sum,
        "min": min(nums),
        "max": max(nums),
        "mean": total_sum / total_count,
    }