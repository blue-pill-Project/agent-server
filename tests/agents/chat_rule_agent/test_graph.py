from collections.abc import AsyncIterator
from pprint import pprint
from typing import Any, Callable
import pytest

from agents.subgraphs.chat_rule_agent.graph import build_generate_chat_rule_graph
from agents.subgraphs.chat_rule_agent.state import (
    Context,
)
from common.config import settings
from common.utils.datetime import get_now
from tests.agents.chat_rule_agent.cases import CHARACTER_CASES, CharacterCase


@pytest.mark.parametrize("case", CHARACTER_CASES, ids=lambda case: case.id)
@pytest.mark.asyncio
async def test_chat_rule_agent(
    case: CharacterCase,
    context_factory: Callable[[CharacterCase], Context],
    chat_rule_agent_report: list[dict[str, Any]],
) -> None:
    graph = build_generate_chat_rule_graph().compile()
    context = context_factory(case)

    report_item: dict[str, Any] = {
        "case_id": case.id,
        "log_room_member_prompt": case.log_room_member_prompt,
        "example_dialogues": case.example_dialogues,
        "relationship": case.relationship,
        "status": "failed",
    }

    try:
        result = await graph.ainvoke(
            {},
            context=context,
        )

        assert result["chat_rule"]

        report_item.update(
            {
                "status": "passed",
                "chat_rule": result.get("chat_rule"),
            }
        )

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"
        raise

    finally:
        chat_rule_agent_report.append(report_item)
