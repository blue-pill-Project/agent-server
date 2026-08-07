from collections.abc import AsyncIterator
from pprint import pprint
import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.subgraphs.search_long_term_memory.graph import (
    build_search_long_term_memory_graph,
)
from agents.subgraphs.search_long_term_memory.state import (
    Context,
    Source,
)
from common.config import settings
from common.utils.datetime import get_now


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
def context() -> Context:
    return Context(
        user_id="1", log_room_id="1", log_room_member_id="2", now=get_now().date()
    )


TEST_SOURCES = [
    # "쪼꼬가 많이 아프네...ㅠㅠ",
    # "하 내 버킷리스트를 이룰수있을까?",
    # "안녕?",
    # "나 지금 너무 높이 올라왔어 무섭네",
    # "오늘 진짜 힘드네",
    "오늘 어디갈까 추천해줘",
]


@pytest.mark.asyncio
@pytest.mark.parametrize("source_text", TEST_SOURCES)
async def test_search_long_term_memory_graph_with_postgres(
    context: Context,
    memory_store: AsyncPostgresStore,
    source_text: str,
) -> None:
    graph = build_search_long_term_memory_graph().compile(
        store=memory_store,
    )

    source = Source(
        purpose="chat",
        source=source_text,
    )

    result = await graph.ainvoke(
        {
            "source": source,
        },
        context=context,
    )

    print("\n//==== Graph result ====//")
    pprint(result)

    assert True
