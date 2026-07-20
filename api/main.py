from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
from agents.weekly_plan_agent.agent import WeeklyPlanAgent
from api.routers import trend, weekly_plan
from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.store.postgres import AsyncPostgresStore
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from common.db.pool import create_db_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = create_db_pool()

    await pool.open()
    await pool.wait(timeout=10)

    try:
        weekly_plan_agent = WeeklyPlanAgent(
            pool=pool,
        )

        weekly_plan_agent.get_graph()

        app.state.db_pool = pool
        app.state.weekly_plan_agent = weekly_plan_agent

        yield

    finally:
        await pool.close()


app = FastAPI(title="Blue Pill Agent Server", lifespan=lifespan)


app.include_router(trend.router)
app.include_router(weekly_plan.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
