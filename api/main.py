from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from agents.chat_rule_agent.agent import ChatRuleAgent
from agents.visual_prompt_reference.agent import VisualPromptReferenceAgent
from agents.weekly_plan_agent.agent import WeeklyPlanAgent
from agents.daily_logs_agent.agent import DailyLogsAgent
from agents.character_chat_agent.agent import CharacterChatAgent
from agents.trend_agent.agent import TrendAgent
from agents.character_prompt_agent.agent import CharacterPromptAgent
from api.routers import (
    daily_logs,
    trend,
    visual_prompt_reference,
    weekly_plan,
    character_chat,
    log_rooms,
    character_prompt,
    chat_rule,
)
from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.store.postgres import AsyncPostgresStore
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from common.db.pool import create_db_pool
from common.logging_config import setup_logging
from common.utils.embedding import get_embeddings
from common.utils.reranker import BgeReranker
from domains.character.repository import CharacterRepository
from domains.daily_plan.repository import DailyPlanRepository
from domains.log_room_member.repository import LogRoomMemberRepository
from domains.trend.repository import TrendRepository
from domains.hourly_log.repository import HourlyLogRepository
from domains.hourly_plan.repository import HourlyPlanRepository
from common.config import settings
from domains.visual_prompt_reference.repository import VisualPromptReferenceRepository
from domains.message.repository import MessageRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작할 때 환경변수 체크
    settings.validate()
    setup_logging()
    pool = create_db_pool()
    reranker = BgeReranker()

    await pool.open()
    await pool.wait(timeout=10)

    try:
        embeddings = get_embeddings()

        store = AsyncPostgresStore(
            pool,
            index={
                "embed": embeddings,
                "dims": 1536,
                "fields": ["content"],
            },
        )

        checkpointer = AsyncPostgresSaver(pool)

        await store.setup()
        await checkpointer.setup()

        trend_repository = TrendRepository(pool)
        daily_plan_repository = DailyPlanRepository(pool)
        log_room_member_repository = LogRoomMemberRepository(pool)
        hourly_log_repository = HourlyLogRepository(pool)
        hourly_plan_repository = HourlyPlanRepository(pool)
        visual_prompt_reference_repository = VisualPromptReferenceRepository(pool)
        character_repository = CharacterRepository(pool)
        message_repository = MessageRepository(pool)

        trend_agent = TrendAgent(
            trend_repository=trend_repository,
        )

        weekly_plan_agent = WeeklyPlanAgent(
            trend_repository=trend_repository,
            daily_plan_repository=daily_plan_repository,
            log_room_member_repository=log_room_member_repository,
        )

        daily_logs_agent = DailyLogsAgent(
            log_room_member_repository=log_room_member_repository,
            daily_plan_repository=daily_plan_repository,
            hourly_log_repository=hourly_log_repository,
            hourly_plan_repository=hourly_plan_repository,
            visual_prompt_reference_repository=visual_prompt_reference_repository,
            message_repository=message_repository,
            store=store,
            reranker=reranker,
        )

        character_chat_agent = CharacterChatAgent(
            log_room_member_repository=log_room_member_repository,
            store=store,
            checkpointer=checkpointer,
            reranker=reranker,
        )

        visual_prompt_reference_agent = VisualPromptReferenceAgent(
            visual_prompt_reference_repository=visual_prompt_reference_repository,
        )

        character_prompt_agent = CharacterPromptAgent()

        chat_rule_agent = ChatRuleAgent(
            character_repository=character_repository,
        )

        trend_agent.get_graph()
        weekly_plan_agent.get_graph()
        daily_logs_agent.get_graph()
        character_chat_agent.get_graph()
        visual_prompt_reference_agent.get_graph()
        character_prompt_agent.get_graph()
        chat_rule_agent.get_graph()

        app.state.reranker = reranker
        app.state.db_pool = pool
        app.state.store = store
        app.state.checkpointer = checkpointer
        app.state.daily_plan_repository = daily_plan_repository
        app.state.trend_agent = trend_agent
        app.state.weekly_plan_agent = weekly_plan_agent
        app.state.daily_logs_agent = daily_logs_agent
        app.state.character_chat_agent = character_chat_agent
        app.state.visual_prompt_reference_agent = visual_prompt_reference_agent
        app.state.character_prompt_agent = character_prompt_agent
        app.state.chat_rule_agent = chat_rule_agent

        yield

    finally:
        await pool.close()


app = FastAPI(title="Blue Pill Agent Server", lifespan=lifespan)


app.include_router(trend.router)
app.include_router(weekly_plan.router)
app.include_router(daily_logs.router)
app.include_router(character_chat.router)
app.include_router(visual_prompt_reference.router)
app.include_router(log_rooms.router)
app.include_router(character_prompt.router)
app.include_router(chat_rule.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
