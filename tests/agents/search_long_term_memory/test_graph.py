from collections.abc import AsyncIterator
from pprint import pprint
from typing import Any, Callable
import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.subgraphs.search_long_term_memory.graph import (
    build_search_long_term_memory_graph,
)
from agents.subgraphs.search_long_term_memory.state import (
    Context,
)
from common.config import settings
from common.utils.datetime import get_now
from tests.agents.search_long_term_memory.cases import SEARCH_LONG_TERM_CASES


@pytest.mark.parametrize("case", SEARCH_LONG_TERM_CASES, ids=lambda case: case.id)
@pytest.mark.asyncio
async def test_search_long_term_memory_graph(
    case: str,
    context_factory: Callable[[list[str]], Context],
    memory_store: AsyncPostgresStore,
    search_long_term_memory_report: list[dict[str, Any]],
) -> None:
    graph = build_search_long_term_memory_graph().compile(
        store=memory_store,
    )

    context = context_factory([case])

    report_item: dict[str, Any] = {
        "case_id": case.id,
        "purpose": case.purpose,
        "source": case.source,
        "status": "failed",
    }

    try:
        result = await graph.ainvoke(
            {
                "source": case,
            },
            context=context,
        )

        assert result["retrieval_query"]

        report_item.update(
            {
                "status": "passed",
                "retrieval_query": result.get("retrieval_query"),
                "search_results": result.get("search_results") or [],
                "reranked_results": result.get("reranked_results") or [],
                "final_long_term_memories": result.get("final_long_term_memories")
                or [],
            }
        )

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"
        raise

    finally:
        search_long_term_memory_report.append(report_item)
