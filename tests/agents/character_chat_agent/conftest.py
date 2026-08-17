import json
from pathlib import Path
from collections.abc import AsyncIterator, Callable
from pprint import pprint
from typing import Any, Iterator
import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore
from agents.character_chat_agent.state import Context
from common.config import settings
from common.utils.datetime import get_current_date, get_now
from tests.agents.character_chat_agent.cases import CHAT_CASES, CharacterChatCase


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
def context_factory() -> Callable[[CharacterChatCase], Context]:
    def create_context(case: CharacterChatCase) -> Context:
        return Context(
            user_id="1",
            log_room_id="1",
            log_room_member_id="2",
            current_date=get_current_date(),
            now=get_now().date(),
            log_room_member_prompt=case.prompt,
            log_room_relationships=case.relationship,
        )

    return create_context


@pytest.fixture
def default_context(
    context_factory: Callable[[CharacterChatCase], Context],
) -> Context:
    return context_factory(CHAT_CASES[0])


# =================================================#
@pytest.fixture(scope="session")
def character_chat_report() -> Iterator[list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []

    yield results

    print("\n\n//========== 🧪 CHARACTER CHAT TEST REPORT ==========//")

    for result in results:
        print(f"\n[{result['status'].upper()}] {result['case_id']}")

        if result["status"] == "failed":
            print(f"error    : {result.get('error')}")
            continue

        # TODO: 결과 프린팅 추가해야함...

    timestamp = get_report_timestamp()
    output_path = Path(
        f"tests/agents/character_chat_agent/results/character_chat_{timestamp}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"\n결과 파일: {output_path}")
