from typing import Any, Callable
from uuid import uuid4
import pytest
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.checkpoint.memory import InMemorySaver
from agents.character_chat_agent.graph import (
    build_character_chat_graph,
)
from agents.character_chat_agent.state import (
    Context,
)
from tests.agents.character_chat_agent.cases import (
    CHARACTER_CHAT_CASES,
    CharacterChatCase,
)


def create_config(case_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": f"daily-logs-{case_id}-{uuid4()}",
        }
    }


@pytest.mark.parametrize("case", CHARACTER_CHAT_CASES, ids=lambda case: case.id)
@pytest.mark.asyncio
async def test_character_chat_graph(
    case: CharacterChatCase,
    context_factory: Callable[[CharacterChatCase], Context],
    memory_store: AsyncPostgresStore,
    character_chat_report: list[dict[str, Any]],
) -> None:
    graph = build_character_chat_graph().compile(
        checkpointer=InMemorySaver(),
        store=memory_store,
    )

    context = context_factory(case)

    report_item: dict[str, Any] = {
        "case_id": case.id,
        "content": case.content,
        "status": "failed",
    }

    try:
        result = await graph.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": case.content,
                    }
                ],
                "long_term_memories": [],
            },
            config=create_config(case.id),
            context=context,
        )

        assert result["messages"][-1]

        report_item.update(
            {
                "status": "passed",
                "long_term_memories": result.get("long_term_memories") or [],
                "reply": result["messages"][-1],
            }
        )

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"
        raise

    finally:
        character_chat_report.append(report_item)
