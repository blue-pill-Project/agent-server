from dotenv import load_dotenv

from agents.trend_agent.agent import TrendAgent


load_dotenv()


from fastapi import FastAPI
from agents.weekly_plan_agent.agent import WeeklyPlanAgent
from api.routers import trend, weekly_plan
from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from common.db.pool import create_db_pool
from domains.daily_plan.repository import DailyPlanRepository
from domains.log_room_member.repository import LogRoomMemberRepository
from domains.trend.repository import TrendRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = create_db_pool()

    await pool.open()
    await pool.wait(timeout=10)

    try:
        # store = AsyncPostgresStore(pool)
        # checkpointer = AsyncPostgresSaver(pool)

        # await store.setup()

        trend_repository = TrendRepository(pool)
        daily_plan_repository = DailyPlanRepository(pool)
        log_room_member_repository = LogRoomMemberRepository(pool)

        trend_agent = TrendAgent(
            trend_repository=trend_repository,
            # store=store
        )

        weekly_plan_agent = WeeklyPlanAgent(
            trend_repository=trend_repository,
            daily_plan_repository=daily_plan_repository,
            log_room_member_repository=log_room_member_repository,
            # store=store
        )

        trend_agent.get_graph()
        weekly_plan_agent.get_graph()

        app.state.db_pool = pool
        app.state.trend_agent = trend_agent
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
