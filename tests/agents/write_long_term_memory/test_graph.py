from typing import Any, Callable
import pytest
from langgraph.store.postgres.aio import AsyncPostgresStore
from agents.subgraphs.write_long_term_memory.graph import (
    build_write_long_term_memory_graph,
)
from agents.subgraphs.write_long_term_memory.state import (
    Context,
)
from tests.agents.write_long_term_memory.cases import WRITE_LONG_TERM_CASES


@pytest.mark.parametrize("case", WRITE_LONG_TERM_CASES, ids=lambda case: case.id)
@pytest.mark.asyncio
async def test_write_long_term_memory_graph(
    case: str,
    context_factory: Callable[[list[str]], Context],
    memory_store: AsyncPostgresStore,
    write_long_term_memory_report: list[dict[str, Any]],
) -> None:
    graph = build_write_long_term_memory_graph().compile(
        store=memory_store,
    )

    context = context_factory([case])

    report_item: dict[str, Any] = {
        "case_id": case.id,
        "source_type": case.source_type,
        "source": case.source,
        "status": "failed",
    }

    try:
        result = await graph.ainvoke(
            {
                "memory_source": case,
            },
            context=context,
        )

        report_item.update(
            {
                "status": "passed",
                "memories": result.get("memories") or [],
                "is_saved_long_term_memory": result.get("is_saved_long_term_memory"),
            }
        )

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"
        raise

    finally:
        write_long_term_memory_report.append(report_item)
