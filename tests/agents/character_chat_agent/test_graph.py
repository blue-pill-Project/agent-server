from collections.abc import Callable
from typing import Any
from uuid import uuid4

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.character_chat_agent.graph import (
    build_character_chat_graph,
)
from agents.character_chat_agent.state import Context

from tests.agents.character_chat_agent.cases import (
    CHAT_CASES,
    CHARACTER_PROMPT_CASES,
    CharacterPromptCase,
)


def create_config(character_id: str) -> dict:
    return {
        "configurable": {
            "thread_id": (f"character-chat-{character_id}-{uuid4()}"),
        }
    }


@pytest.mark.parametrize(
    "character",
    CHARACTER_PROMPT_CASES,
    ids=lambda character: character.id,
)
@pytest.mark.asyncio
async def test_character_chat_graph(
    character: CharacterPromptCase,
    context_factory: Callable[
        [CharacterPromptCase],
        Context,
    ],
    memory_store: AsyncPostgresStore,
    character_chat_report: list[dict[str, Any]],
) -> None:
    # ========================================================
    # 캐릭터 하나당 checkpointer 하나
    # ========================================================

    checkpointer = InMemorySaver()

    graph = build_character_chat_graph().compile(
        checkpointer=checkpointer,
        store=memory_store,
    )

    # ========================================================
    # 캐릭터 하나당 context 하나
    # ========================================================

    context = context_factory(character)

    # ========================================================
    # 캐릭터 하나당 thread 하나
    #
    # 이 config를 아래 CHAT_CASES 전체에서 공유해야
    # checkpoint가 이어진다.
    # ========================================================

    config = create_config(character.id)

    conversation: list[dict[str, Any]] = []

    report_item: dict[str, Any] = {
        "character_id": character.id,
        "name": character.name,
        "relationship": character.relationship,
        "status": "failed",
        "conversation": conversation,
    }

    try:
        # ====================================================
        # 하나의 캐릭터와 연속 대화
        # ====================================================

        for turn, chat in enumerate(
            CHAT_CASES,
            start=1,
        ):
            result = await graph.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": chat.content,
                        }
                    ],
                    "long_term_memories": [],
                    "chat_rule": character.chat_rule,
                },
                config=config,
                context=context,
            )

            assert result["messages"]
            assert result["messages"][-1]

            reply = result["messages"][-1].content

            conversation.append(
                {
                    "turn": turn,
                    "chat_id": chat.id,
                    "user": chat.content,
                    "reply": reply,
                    "long_term_memories": (result.get("long_term_memories") or []),
                }
            )

        report_item["status"] = "passed"

    except Exception as error:
        report_item["error"] = f"{type(error).__name__}: {error}"

        raise

    finally:
        character_chat_report.append(report_item)
