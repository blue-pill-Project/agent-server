from fastapi import FastAPI
from api.routers import trend

app = FastAPI(title="Blue Pill Agent Server")


app.include_router(trend.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
