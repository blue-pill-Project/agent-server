from collections.abc import AsyncIterator, Callable
from textwrap import dedent

import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore
import json
from pathlib import Path
from typing import Any
from agents.daily_logs_agent.state import Context
from common.config import settings
from common.db.pool import create_db_pool
from common.utils.datetime import (
    get_current_date,
    get_current_month,
    get_now,
    get_timeslot_label,
)
from common.utils.reranker import BgeReranker
from domains.visual_prompt_reference.repository import (
    VisualPromptReferenceRepository,
)

from tests.agents.daily_logs_agent.cases import DAILY_LOG_CASES, DailyLogCase


TEST_IMAGE_URL = (
    "https://i.pinimg.com/736x/91/5e/0e/915e0e09e60665b3b653b7f8d7a30113.jpg"
)


def get_report_timestamp() -> str:
    return get_now().strftime("%Y%m%d_%H%M%S")


@pytest_asyncio.fixture
async def visual_prompt_reference_repository() -> AsyncIterator[
    VisualPromptReferenceRepository
]:
    pool = create_db_pool()
    await pool.open()

    try:
        await pool.wait(timeout=10)
        yield VisualPromptReferenceRepository(pool)
    finally:
        await pool.close()


@pytest_asyncio.fixture
async def memory_store() -> AsyncIterator[AsyncPostgresStore]:
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    async with AsyncPostgresStore.from_conn_string(
        settings.DB_URL,
        index={
            "embed": embeddings,
            "dims": 1536,
            "fields": ["content"],
        },
    ) as store:
        await store.setup()
        yield store


@pytest.fixture
def context_factory(
    visual_prompt_reference_repository: VisualPromptReferenceRepository,
) -> Callable[[DailyLogCase], Context]:
    def create_context(case: DailyLogCase) -> Context:
        timeslot = int(case.timeslot)

        return Context(
            user_id="1",
            log_room_id="1",
            log_room_member_id="3",
            now=get_now(),
            current_month=get_current_month(),
            current_date=get_current_date(),
            timeslot=case.timeslot,
            timeslot_label=get_timeslot_label(timeslot),
            previous_plans=list(case.previous_plans),
            log_room_member_prompt=case.character_prompt,
            today_plan=case.today_plan,
            image_url=TEST_IMAGE_URL,
            visual_prompt_reference_repository=visual_prompt_reference_repository,
            reranker=BgeReranker(),
        )

    return create_context


@pytest.fixture
def default_context(
    context_factory: Callable[[DailyLogCase], Context],
) -> Context:
    return context_factory(DAILY_LOG_CASES[0])


@pytest.fixture(scope="session")
def hourly_plan_report() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    yield results

    results.sort(key=lambda item: item["case_id"])

    print("\n\n//========== 🧪 DAILY LOG TEST REPORT ==========//")

    for result in results:
        print(f"\n[{result['case_id']}]")
        print(f"timeslot    : {result['timeslot']}")
        print(f"title       : {result['hourly_plan']['title']}")
        print(f"description : {result['hourly_plan']['description']}")
        print(f"outfit      : {result['hourly_plan']['outfit']}")
        print(f"location    : {result['hourly_plan']['location']}")
    timestamp = get_report_timestamp()
    output_path = Path(
        f"tests/agents/daily_logs_agent/results/hourly_plan_report_{timestamp}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n결과 파일: {output_path}")


@pytest.fixture(scope="session")
def hourly_log_report() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    yield results

    results.sort(key=lambda item: item["case_id"])

    passed_count = sum(result["status"] == "passed" for result in results)
    failed_count = len(results) - passed_count

    print("\n\n//========== 🧪 DAILY LOG GRAPH REPORT ==========//")
    print(f"total  : {len(results)}")
    print(f"passed : {passed_count}")
    print(f"failed : {failed_count}")

    for result in results:
        print(f"\n[{result['status'].upper()}] {result['case_id']}")
        print(f"timeslot : {result['timeslot']}")

        if result["status"] == "failed":
            print(f"error    : {result.get('error')}")
            continue

        hourly_log = result["hourly_log"]
        hourly_plan = hourly_log["hourly_plan"]

        print(f"title       : {hourly_plan['title']}")
        print(f"description : {hourly_plan['description']}")
        print(f"outfit      : {hourly_plan['outfit']}")
        print(f"location    : {hourly_plan['location']}")
        print(f"image       : {hourly_log['log_image_url']}")

        print("log_text:")
        print(
            json.dumps(
                hourly_log["log_text"],
                ensure_ascii=False,
                indent=2,
            )
        )

        memories = result.get("long_term_memories", [])
        print(f"memories    : {len(memories)}개")

        if memories:
            for index, memory in enumerate(memories, start=1):
                print(f"  {index}. {memory}")

    timestamp = get_report_timestamp()
    output_path = Path(
        f"tests/agents/daily_logs_agent/results/hourly_log_report_{timestamp}.json"
    )
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    output_path.write_text(
        json.dumps(
            results,
            ensure_ascii=False,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(f"\n결과 파일: {output_path}")
