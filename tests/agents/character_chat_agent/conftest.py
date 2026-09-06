import json
from pathlib import Path
from collections.abc import AsyncIterator, Callable
from typing import Any, Iterator
from uuid import uuid4

import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.character_chat_agent.state import Context
from common.config import settings
from common.utils.datetime import get_current_date, get_now
from common.utils.reranker import BgeReranker
from tests.agents.character_chat_agent.cases import (
    CHARACTER_PROMPT_CASES,
    CharacterPromptCase,
)


def get_report_timestamp() -> str:
    return get_now().strftime("%Y%m%d_%H%M%S")


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
def context_factory() -> Callable[[CharacterPromptCase], Context]:
    def create_context(character: CharacterPromptCase) -> Context:
        # 테스트 실행마다 새로운 로그방을 사용해서
        # 이전 테스트의 장기기억과 격리한다.
        test_log_room_id = str(uuid4().int % 2_000_000_000)

        return Context(
            user_id="1",
            log_room_id=test_log_room_id,
            log_room_member_id="2",
            current_date=get_current_date(),
            now=get_now().date(),
            log_room_member_prompt=character.prompt,
            log_room_relationships=character.relationship,
            reranker=BgeReranker(),
        )

    return create_context


@pytest.fixture
def default_context(
    context_factory: Callable[[CharacterPromptCase], Context],
) -> Context:
    return context_factory(CHARACTER_PROMPT_CASES[0])


# ============================================================
# CHARACTER CHAT REPORT
# ============================================================


@pytest.fixture(scope="session")
def character_chat_report() -> Iterator[list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []

    yield results

    print("\n\n//========== 🧪 CHARACTER CHAT TEST REPORT ==========//")

    for result in results:
        print(
            f"\n"
            f"[{result['status'].upper()}] "
            f"{result['character_id']} / {result['name']}"
        )

        print(f"relationship : {result['relationship']}")

        if result["status"] == "failed":
            print(f"error        : {result.get('error')}")
            continue

        for conversation in result["conversation"]:
            print(f"\n--- TURN {conversation['turn']} ---")

            print(f"USER      : {conversation['user']}")

            print(f"CHARACTER : {conversation['reply']}")

            memories = conversation.get("long_term_memories")

            if memories:
                print(f"MEMORIES  : {memories}")

    timestamp = get_report_timestamp()

    output_path = Path(
        f"tests/agents/character_chat_agent/results/character_chat_{timestamp}.json"
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
