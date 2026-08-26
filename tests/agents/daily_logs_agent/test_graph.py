from typing import Any
from collections.abc import Callable
from uuid import uuid4
import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.daily_logs_agent.graph import build_daily_logs_graph
from agents.daily_logs_agent.state import Context, HourlyLog
from tests.agents.daily_logs_agent.cases import (
    DAILY_LOG_CASES,
    DailyLogCase,
)


def create_config(case_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": f"daily-logs-{case_id}-{uuid4()}",
        }
    }


@pytest.mark.parametrize(
    "case",
    DAILY_LOG_CASES,
    ids=lambda case: case.id,
)
@pytest.mark.asyncio
async def test_daily_logs_graph(
    case: DailyLogCase,
    context_factory: Callable[[DailyLogCase], Context],
    memory_store: AsyncPostgresStore,
    hourly_log_report: list[dict[str, Any]],
) -> None:
    graph = build_daily_logs_graph().compile(
        checkpointer=InMemorySaver(),
        store=memory_store,
    )
    context = context_factory(case)

    report_item: dict[str, Any] = {
        "case_id": case.id,
        "timeslot": case.timeslot,
        "today_plan": case.today_plan,
        "previous_plans": list(case.previous_plans),
        "status": "failed",
    }

    try:
        result = await graph.ainvoke(
            {},
            config=create_config(case.id),
            context=context,
        )

        raw_hourly_log = result.get("hourly_log")

        assert raw_hourly_log is not None, (
            f"{case.id}: graph result에 hourly_log가 없습니다.\n"
            f"result keys: {list(result.keys())}"
        )

        hourly_log = HourlyLog.model_validate(raw_hourly_log)

        assert str(hourly_log.timeslot) == str(case.timeslot)

        hourly_plan = hourly_log.hourly_plan

        assert str(hourly_plan.timeslot) == str(case.timeslot)
        assert hourly_plan.title.strip()
        assert hourly_plan.description.strip()
        assert hourly_plan.outfit.strip()
        assert hourly_plan.location.strip()

        assert hourly_log.log_image_url.strip()

        log_text = hourly_log.log_text.model_dump(mode="json")
        assert log_text

        assert hourly_log.hourly_plan == result["hourly_plan"]
        assert hourly_log.log_text == result["log_text"]
        assert hourly_log.log_image_url == result["log_image_url"]

        report_item.update(
            {
                "status": "passed",
                "hourly_log": hourly_log.model_dump(mode="json"),
                "long_term_memories": result.get("long_term_memories") or [],
                "related_chats": result.get("related_chats") or "",
                "hourly_plan_description": result["hourly_plan"].description,
                "image_reference": result.get("image_reference"),
                "image_reference_prompt": result.get("image_reference_prompt"),
                "image_prompt": result.get("image_prompt"),
                "is_saved_long_term_memory": result.get("is_saved_long_term_memory"),
                "visual_prompt_reference_search_query": result.get(
                    "visual_prompt_reference_search_query"
                ),
            }
        )

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"
        raise

    finally:
        hourly_log_report.append(report_item)
