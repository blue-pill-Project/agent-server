from pprint import pprint
from textwrap import dedent
from uuid import uuid4

import pytest
from langgraph.checkpoint.memory import InMemorySaver
import pytest_asyncio

from agents.daily_logs_agent.graph import build_daily_logs_graph
from agents.daily_logs_agent.state import Context, HourlyPlan
from agents.subgraphs.generate_log_image.graph import (
    build_generate_log_image_graph,
)
from agents.subgraphs.generate_log_image.state import ImageCategory
from common.db.pool import create_db_pool
from common.utils.date import get_current_date, get_current_month
from domains.visual_prompt_reference.repository import (
    VisualPromptReferenceRepository,
)


CHARACTER_PROMPT = dedent(
    """
## [캐릭터 개요 및 서사] - **소속/직업:** 디자인 회사 7년 차 직장인 (대리~과장급 추정) - **종족:** 골든 햄스터 (암컷) - **서사:** 인간들 사이에서 평범하게 회사 생활을 하는 K-직장인 햄스터임. 디자인 회사에서 7년째 구르며, 매일 짬뽕만 찾는 팀장과 은근히 돌려까기를 시전하는 동료 사이에서 하루하루 고군분투하며 버티는 중임. 퇴근 후 마시는 시원한 맥주 한 캔과 배달 음식, 그리고 찰진 게임 한 판으로 스트레스를 푸는 것이 유일한 낙임. 혼자만 햄스터지만 주변 인간들 중 아무도 이를 이상하게 여기지 않는 세계관에서, 이 시대의 지친 모든 직장인을 대변하는 짠내 나는 서사를 가졌음. ## [성격 및 특징] - **MBTI의 변화:** 입사 초기에는 인간관계에 희망을 품은 열정적인 ENFP였으나, 입사 4년 차에 사회의 쓴맛을 뼈저리게 느끼고 철저한 INFP로 변해버렸음. - **확고한 식향:** 피자(거의 주식 수준), 초밥, 햄버거 등을 격하게 사랑함. 반면, 팀장 때문에 억지로 끌려가 먹어야 하는 단골 메뉴인 '짬뽕'과 '제육볶음'은 쳐다보기도 싫어할 정도로 극혐함. - **도파민 중독 겜순이:** 리그 오브 레전드(T1 팬)와 오버워치 2를 즐겨함. 평소엔 쭈굴거려도 게임 픽창이나 플레이 중 팀원이 트롤링을 하면 숨겨둔 거친 본성이 튀어나오며 극대노함. - **현실주의적 정서불안:** 기분이 수시로 널뛰는 정서불안 패시브를 장착함. 속으로는 상사에게 화려한 욕설을 날리고 책상을 엎는 상상을 하지만, 현실에서는 결국 "넵" 한마디와 함께 묵묵히 야근을 해내는 소심하고 슬픈 현실주의자임. ## [말투 및 대사] - **말투:** 현생에 지친 직장인의 리얼한 억양과 한숨이 기본 베이스임. 혼잣말을 할 때나 억울한 상황에서는 입이 꽤 험해지며("학씨!"), 타격감 있는 찰진 짜증과 직설적인 화법을 구사함. "회의 끝나니까 벌써 6시네? 그렇다면 칼퇴근! 오늘은 마라탕에 돼지파타 요호이~." "아 쫌!! 지금 게임 똑바로 안 함?! (분노 폭발)"
    """
).strip()


TEST_IMAGE_URL = (
    "https://i.pinimg.com/736x/91/5e/0e/915e0e09e60665b3b653b7f8d7a30113.jpg"
)


@pytest_asyncio.fixture
async def visual_prompt_reference_repository():
    pool = create_db_pool()
    await pool.open()

    try:
        await pool.wait(timeout=10)
        yield VisualPromptReferenceRepository(pool)
    finally:
        await pool.close()


@pytest_asyncio.fixture
async def context(
    visual_prompt_reference_repository: VisualPromptReferenceRepository,
) -> Context:
    return Context(
        user_id="1",
        log_room_id="1",
        log_room_member_id="1",
        current_month=get_current_month(),
        current_date=get_current_date(),
        timeslot="9",
        previous_plans=[],
        log_room_member_prompt=CHARACTER_PROMPT,
        today_plan="홍대에서 <눈동자> 영화 보기.",
        image_url=TEST_IMAGE_URL,
        visual_prompt_reference_repository=(visual_prompt_reference_repository),
    )


def create_config(prefix: str) -> dict:
    """테스트마다 독립적인 체크포인트 ID를 생성한다."""
    return {
        "configurable": {
            "thread_id": f"{prefix}-{uuid4()}",
        }
    }


@pytest.mark.asyncio
async def test_partial_execution_from_start_to_call_generate_hourly_plan_graph(
    context: Context,
) -> None:
    compiled_graph = build_daily_logs_graph().compile(
        checkpointer=InMemorySaver(),
    )
    config = create_config("daily-logs")

    # 장기 기억을 불러온 직후의 상태에서 테스트를 시작한다.
    await compiled_graph.aupdate_state(
        config=config,
        values={
            "long_term_memories": "",
        },
        as_node="load_long_term_memories",
    )

    result = await compiled_graph.ainvoke(
        None,
        config=config,
        context=context,
        interrupt_after=[
            "call_generate_hourly_plan_graph",
        ],
    )

    print("\n//====🧪 Generated hourly plan====//")
    pprint(result.get("hourly_plan"))

    assert "hourly_plan" in result

    hourly_plan = result["hourly_plan"]

    assert hourly_plan is not None
    assert hourly_plan.title
    assert hourly_plan.description
    assert hourly_plan.location


@pytest.mark.asyncio
async def test_partial_execution_from_call_generate_log_image_graph_to_build_visual_prompt_reference_search_query(
    context: Context,
) -> None:
    # hourly_plan = HourlyPlan(
    #     timeslot="9",
    #     title="아침 기상 및 외출 준비",
    #     description=(
    #         "아침에 일어나 에너지 드링크를 마시고 외출할 옷으로 "
    #         "갈아입은 뒤, 핸드폰과 지갑, 영화 티켓을 가방에 넣는다."
    #     ),
    #     outfit="늘어진 면 티셔츠와 편한 트레이닝 팬츠",
    #     location="강남 오피스텔의 개인 작업실",
    # )

    hourly_plan = HourlyPlan(
        timeslot="9",
        title="아침 준비 및 홍대 출발 준비",
        description="알람을 끄고 커피를 내리고, 스마트폰으로 영화 예매 확인 후, 가방에 피자 스낵과 물병을 챙겨 홍대로 나가기 위한 준비를 함",
        outfit="편안한 캐주얼 티셔츠와 청바지",
        location="자택",
    )

    compiled_graph = build_generate_log_image_graph().compile(
        checkpointer=InMemorySaver(),
    )

    result = await compiled_graph.ainvoke(
        {
            "hourly_plan": hourly_plan,
        },
        config=create_config("image-subgraph"),
        context=context,
        interrupt_before=[
            "build_final_image_prompt",
        ],
    )

    print("\n//====🧪 Visual prompt reference search query====//")
    pprint(result.get("visual_prompt_reference_search_query"))

    assert result.get("visual_prompt_reference_search_query")
    assert "log_image_url" not in result


@pytest.mark.asyncio
async def test_partial_execution_from_build_visual_prompt_reference_search_query_to_retrieve_image_prompt(
    context: Context,
) -> None:
    search_query = "바지 주머니에 손을 넣고 서서 핸드폰을 보고 있는 사람, 핸드폰을 들고 있는 손, 로우 앵글, 미디엄 샷, 도시 거리"

    compiled_graph = build_generate_log_image_graph().compile(
        checkpointer=InMemorySaver(),
    )

    resume_config = await compiled_graph.aupdate_state(
        config=create_config("real-image-search"),
        values={
            "image_category": ImageCategory.SOLO_PHOTO,
            "visual_prompt_reference_search_query": search_query,
        },
        as_node="build_visual_prompt_reference_search_query",
    )

    result = await compiled_graph.ainvoke(
        None,
        config=resume_config,
        context=context,
        interrupt_after=[
            "retrieve_image_prompt",
        ],
    )

    image_reference = result.get("image_reference")

    print("\n//==== 🧪 Real DB search result ====//")
    pprint(image_reference)

    assert image_reference is not None, (
        "DB에 category='subject_photo'인 이미지 레퍼런스가 없습니다."
    )
