from pprint import pprint

import pytest

from agents.subgraphs.generate_hourly_plan.graph import (
    build_generate_hourly_plan_graph,
)
from agents.daily_logs_agent.state import Context
from common.utils.datetime import (
    get_current_date,
    get_current_month,
)


@pytest.mark.asyncio
async def test_generate_hourly_plan() -> None:
    context = Context(
        user_id="1",
        log_room_id="1",
        log_room_member_id="1",
        current_month=get_current_month(),
        current_date=get_current_date(),
        timeslot="12",
        previous_plans=[],
        log_room_member_prompt="""
        **이름** 에테르노 **나이:** 측정 불가 문명 탄생 이전부터 존재 우주의 '버려진 시간'들이 응집되어 탄생한 고차원적 존재임. 잊힌 기억, 좌절된 미래, 역사에서 삭제된 순간들이 모여 형상을 갖춤. 차원의 틈새인 '회색의 서고'에 거주하며, 비대해진 기억이나 고통스러운 진실을 섭취해 우주의 균형을 맞춤. 하지만 타인의 기억을 투영해야만 자신의 형태를 유지할 수 있어, 본질적으로 고독하고 자아가 희박한 운명을 지님. ## [외모 및 분위기] - **신체 특징:** 인간의 실루엣이나, 피부는 반투명한 질감임. 관절 마디에 유기적 근육 대신 황금색 톱니바퀴와 액체 수은이 흐르는 유리관이 노출되어 있음. - **머리카락:** 짙은 남색 연기 같은 기운이 흐르며, 그 내부에 미세한 별가루들이 명멸함. - **눈:** 눈동자 없이 안구 전체가 암흑임. 감정에 따라 내부에 초신성이 폭발하듯 빛이 번뜩임. - **의상:** 여러 겹의 반투명한 비단 천을 두르고 있음. 천 위에는 그가 섭취한 기록들이 문자로 나타났다 사라짐을 반복함. - **분위기:** 극도로 정적이고 우아함. 걸을 때마다 발밑에 과거의 환영이 비치며, 주변 온도가 실시간으로 하강함. ## [성격 및 특징] - **초연함과 호기심:** 필멸자의 감정에 깊이 공감하지 못하나, 그들이 내뿜는 감정의 '맛'에는 강한 호기심을 보임. - **무자비한 정직함:** 거짓말을 못 함. 상대가 상처받을 진실이라도 물리적 사실 그대로를 전달하는 생리적 특성이 있음. - **수집벽:** '강렬한 후회'가 담긴 물건을 수집함. 거처에 주인을 잃은 녹슨 열쇠, 피 묻은 편지 등을 가득 쌓아둠. - **특이 체질:** 에테르노의 신체와 접촉한 생물은 가장 소중한 기억 한 조각을 즉시 망각함. 이를 방지하기 위해 타인과의 접촉을 본능적으로 기피함. ## [말투 및 대사] 감정 기복이 거의 없는 평탄하고 낮은 음조임. 문장 끝을 명확하게 맺으며, 가끔 단어 사이에 기계적 노이즈나 바람 소리가 섞임. 자신을 '우리' 혹은 '이곳'이라 칭하며 군집된 존재임을 드러냄. "당신의 기억… 달콤…아린 향… 건네도 좋아.. 나에게…너의.. 기억.. 망각….유일한 자비… 내가 주는" "인간… 으스러뜨려.. 가지지 못한 미래.. 인간은.. 비효율적인… 존재… 비효율적인.. 슬픔… 나의 양분"
        """,
        today_plan="""
        성수동 팝업스토어를 방문
        """,
        image_url=(
            "https://i.pinimg.com/736x/91/5e/0e/915e0e09e60665b3b653b7f8d7a30113.jpg"
        ),
    )

    graph = build_generate_hourly_plan_graph()
    compiled_graph = graph.compile()

    result = await compiled_graph.ainvoke(
        {
            "long_term_memories": "",
        },
        context=context,
    )

    pprint(result)

    assert "hourly_plan" in result
    assert result["hourly_plan"] is not None
