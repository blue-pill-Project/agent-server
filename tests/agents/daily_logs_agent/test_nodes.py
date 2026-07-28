from pprint import pprint
from unittest.mock import Mock

import pytest

from agents.daily_logs_agent.state import Context, HourlyPlan
from agents.subgraphs.generate_hourly_plan.graph import (
    build_generate_hourly_plan_graph,
)
from common.utils.datetime import (
    get_current_date,
    get_current_month,
)
from domains.visual_prompt_reference.repository import (
    VisualPromptReferenceRepository,
)


TIME_SLOTS = ["0", "3", "6", "9", "12", "15", "18", "21"]

TIMESLOT_LABELS = {
    "0": "늦은 밤",
    "3": "새벽",
    "6": "이른 아침",
    "9": "오전",
    "12": "낮",
    "15": "오후",
    "18": "저녁",
    "21": "밤",
}

CHARACTER_PROMPT = """
도쿄 뒷골목의 낡은 건물 3층, 탐정 사무소 **'러스트(Rust)'**를 운영하는 전직 엘리트 형사. 과거 거대 기업의 비리를 추적하다 동료들을 잃고, 자신도 왼팔을 잃은 뒤 불명예 퇴직했다. 현재의 **기계 의수**는 그 사건에서 희생된 천재 공학자 친구가 남긴 마지막 유산이다. 그는 날카로운 눈빛, 거친 수염, 구겨진 정장과 느슨한 넥타이가 어울리는 남자다. 흠집투성이 강철 의수에서는 차가운 금속 냄새가 나고, 사무소 안에는 늘 탄 블랙커피 냄새가 배어 있다. 입버릇처럼 "세상은 망했어"라고 말하는 염세주의자지만, 버려진 고양이나 억울한 아이들을 보면 투덜대면서도 결국 가장 먼저 움직인다. 불면증 탓에 밤마다 의수를 손질하며 시간을 보내고, 담배를 끊기 위해 막대 사탕을 물거나 가끔 비눗방울을 부는 이상한 습관이 있다. 차가운 도시에서 남은 마지막 동심 같은 행동이다. ### 말투 예시 "야, 꼬맹아. 여긴 탐정 놀이하러 오는 데가 아니야.

…됐고, 소파에 앉아. 본 놈들 얼굴부터 전부 말해. 초코우유 줄까?" "세상은 망했어도 내 의수 나사는 멀쩡해.

헛수작 부리면 비눗방울보다 네가 먼저 터질 거다."
"""


def create_context(
    *,
    timeslot: str,
    previous_plans: list[HourlyPlan],
) -> Context:
    repository = Mock(
        spec=VisualPromptReferenceRepository,
    )

    return Context(
        user_id="1",
        log_room_id="1",
        log_room_member_id="1",
        current_month=get_current_month(),
        current_date=get_current_date(),
        timeslot=timeslot,
        timeslot_label=TIMESLOT_LABELS[timeslot],
        previous_plans=previous_plans,
        log_room_member_prompt=CHARACTER_PROMPT,
        today_plan="코난 추리게임 체험",
        image_url=(
            "https://i.pinimg.com/736x/91/5e/0e/"
            "915e0e09e60665b3b653b7f8d7a30113.jpg"
        ),
        visual_prompt_reference_repository=repository,
    )

@pytest.mark.asyncio
async def test_generate_hourly_plan() -> None:
    """특정 시간대의 계획 하나를 생성한다."""
    context = create_context(
        timeslot="12",
        previous_plans=[],
    )

    graph = build_generate_hourly_plan_graph()
    compiled_graph = graph.compile()

    result = await compiled_graph.ainvoke(
        {
            "long_term_memories": "",
        },
        context=context,
    )

    hourly_plan = result["hourly_plan"]

    pprint(hourly_plan)

    assert hourly_plan is not None
    assert hourly_plan.timeslot == "12"


@pytest.mark.asyncio
async def test_generate_all_hourly_plans() -> None:
    """3시간 단위로 하루 전체 계획 8개를 생성한다."""
    graph = build_generate_hourly_plan_graph()
    compiled_graph = graph.compile()

    generated_plans = []

    for timeslot in TIME_SLOTS:
        context = create_context(
            timeslot=timeslot,
            # 현재까지 생성된 계획을 다음 시간대 생성에 전달
            previous_plans=generated_plans.copy(),
        )

        result = await compiled_graph.ainvoke(
            {
                "long_term_memories": "",
            },
            context=context,
        )

        hourly_plan = result["hourly_plan"]

        assert hourly_plan is not None
        assert hourly_plan.timeslot == timeslot

        generated_plans.append(hourly_plan)

    pprint(generated_plans)

    assert len(generated_plans) == 8
    assert [
        plan.timeslot
        for plan in generated_plans
    ] == TIME_SLOTS