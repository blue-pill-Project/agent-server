import json
from pathlib import Path
from collections.abc import AsyncIterator, Callable
from pprint import pprint
from typing import Any
import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore
from agents.subgraphs.search_long_term_memory.state import Context
from common.config import settings
from common.utils.datetime import get_now


from tests.agents.search_long_term_memory.cases import SEARCH_LONG_TERM_CASES


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
        settings.DATABASE_URL,
        index={
            "embed": embeddings,
            "dims": 1536,
            "fields": ["content"],
        },
    ) as store:
        await store.setup()
        yield store


@pytest.fixture
def context_factory() -> Callable[[list[str]], Context]:
    def create_context(case: list[str]) -> Context:
        return Context(
            user_id="1", log_room_id="1", log_room_member_id="2", now=get_now().date()
        )

    return create_context


@pytest.fixture
def default_context(
    context_factory: Callable[[list[str]], Context],
) -> Context:
    return context_factory(SEARCH_LONG_TERM_CASES[0])


# =================================================#
@pytest.fixture(scope="session")
def search_long_term_memory_report() -> Iterator[list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []

    yield results

    print("\n\n//========== 🧪 SEARCH LONG TERM MEMORY TEST REPORT ==========//")

    for result in results:
        print(f"\n[{result['status'].upper()}] {result['case_id']}")

        if result["status"] == "failed":
            print(f"error    : {result.get('error')}")
            continue

        #TODO: 결과 프린팅 수정해야함...
        # retrieval_query = result["retrieval_query"]
        # search_results = result["search_results"]
        # reranked_results = result["reranked_results"]
        # final_long_term_memories = result["final_long_term_memories"]

        # print("retrieval_query\n")
        # print(f"should_search       : {retrieval_query['should_search']}")
        # print(f"retrieval_query     : {retrieval_query['retrieval_query']}")
        # print(f"kind_hint           : {retrieval_query['kind_hint']}")

        # print("search_results\n")
        # if search_results:
        #     for search_result in enumerate(search_results, start=1):
        #         print(f"should_search       : {search_result['should_search']}")
        #         print(f"retrieval_query     : {search_result['retrieval_query']}")
        #         print(f"kind_hint           : {search_result['kind_hint']}")

        # print("reranked_results\n")
        # if reranked_results:
        #     for reranked_result in enumerate(reranked_results, start=1):
        #         print(f"content         : {reranked_result['content']}")
        #         print(f"score           : {reranked_result['score']}")
        #         print(f"original_index  : {reranked_result['original_index']}")

    timestamp = get_report_timestamp()
    output_path = Path(
        f"tests/agents/search_long_term_memory/results/search_report_{timestamp}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"\n결과 파일: {output_path}")
