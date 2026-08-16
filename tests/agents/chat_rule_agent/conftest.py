import json
from pathlib import Path
from collections.abc import AsyncIterator, Callable
from pprint import pprint
from typing import Any, Iterator
import pytest
from agents.subgraphs.chat_rule_agent.state import Context
from common.config import settings
from common.utils.datetime import get_now


from tests.agents.chat_rule_agent.cases import CHARACTER_CASES, CharacterCase


def get_report_timestamp() -> str:
    return get_now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture
def context_factory() -> Callable[[CharacterCase], Context]:
    def create_context(case: CharacterCase) -> Context:
        return Context(
            log_room_member_prompt=case.log_room_member_prompt,
            example_dialogues=case.example_dialogues,
            relationship=case.relationship,
        )

    return create_context


@pytest.fixture
def default_context(
    context_factory: Callable[[CharacterCase], Context],
) -> Context:
    return context_factory(CHARACTER_CASES[0])


# =================================================#
@pytest.fixture(scope="session")
def chat_rule_agent_report() -> Iterator[list[dict[str, Any]]]:
    results: list[dict[str, Any]] = []

    yield results

    print("\n\n//========== 🧪 CHAT RULE AGENT TEST REPORT ==========//")

    for result in results:
        print(f"\n[{result['status'].upper()}] {result['case_id']}")

        if result["status"] == "failed":
            print(f"error    : {result.get('error')}")
            continue

    # TODO: 결과 프린팅 추가해야함...
    timestamp = get_report_timestamp()
    output_path = Path(
        f"tests/agents/chat_rule_agent/results/chat_rule_agent_{timestamp}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )

    print(f"\n결과 파일: {output_path}")
