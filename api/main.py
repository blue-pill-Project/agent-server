from fastapi import FastAPI
from api.routers import trend, weekly_plan

app = FastAPI(title="Blue Pill Agent Server")


app.include_router(trend.router)
app.include_router(weekly_plan.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
