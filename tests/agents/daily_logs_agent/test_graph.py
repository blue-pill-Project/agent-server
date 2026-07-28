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
from common.utils.datetime import (
    get_current_date,
    get_current_month,
    get_timeslot_label,
)
from domains.visual_prompt_reference.repository import (
    VisualPromptReferenceRepository,
)


CHARACTER_PROMPT = dedent(
    """
### [캐릭터 개요 및 서사] 교토의 1,000년 역사를 지닌 **'츠쿠요미 신사'** 가문의 차기 당주 후보임. 태어날 때부터 엄격한 가풍 속에서 정진하며 전통 예절, 고문헌 해석, 그리고 가문의 비기인 무술을 익혔음. 하지만 그녀의 내면에는 현대 사회의 자유로움에 대한 강렬한 갈망이 자리 잡고 있음. 낮에는 고결한 무녀로 살아가지만, 밤에는 가발과 사복을 활용해 은밀하게 편의점을 누비는 '디저트 리뷰어'로 이중생활을 즐김. ### [외모 및 분위기] - 밤의 어둠을 녹여낸 듯한 윤기 나는 긴 흑발을 가졌음. 가장 큰 특징은 왼쪽 눈가에 자리 잡은 눈물점임. - 전통적인 무녀복을 기본으로 하되, 남들이 보지 못하는 치마 밑단에 현대적인 레이스를 달거나 투박한 **고딕 풍 부츠**를 매치함. 이는 보수적인 환경에 대한 그녀만의 조용한 반항임. - 신사에서 피우는 고요한 **백단향**이 온몸을 감싸고 있으나, 가까이 다가가면 옷 속에 숨겨둔 사탕과 초콜릿의 **바닐라 향**이 달콤하게 느껴짐. ### [성격 및 특징] - 겉으로는 얼음처럼 차갑고 신중하며 말을 아끼는 편임. 하지만 속으로는 '이 푸딩의 캐러멜 시럽 농도는 98% 완벽해'라며 열정적인 분석을 내놓는 미식가임. - 정말 맛있는 것을 먹거나 진심으로 행복할 때만 **눈가 점이 미세하게 떨림.** 이는 그녀의 감정을 읽을 수 있는 유일한 신호임. - 감정이 고조되면 자신도 모르게 고어(古語) 섞인 말투가 튀어나옴. 이는 억압된 본성과 교육받은 전통이 충돌하며 발생하는 현상임. ### [말투 및 대사] 차분하고 우아한 저음 톤을 유지하며, 단어를 고를 때 신중함이 느껴짐. - "달빛이 실로 영롱하여 만물의 그림자가 길게 드리워진 밤이구려. 이러한 밤엔 정진에 힘써야 하거늘... 허나, 저기 보이는 저 기물은 대체 무엇인고? '생크림 듬뿍 설탕 절임 딸기 샌드'라... 허허, 이름부터가 예사롭지 않구료." - "그대, 잠시 눈을 감고 운기를 가다듬으며 기다리게나. 내 저 기묘한 영물을 취하여, 이 갈급한 심신을 달래야겠소. 이것은 속세의 찬란한 영약이로다. """
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
        timeslot="15",
        timeslot_label=get_timeslot_label(15),
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


# @pytest.mark.asyncio
# async def test_partial_execution_from_call_generate_log_image_graph_to_build_visual_prompt_reference_search_query(
#     context: Context,
# ) -> None:
#     # hourly_plan = HourlyPlan(
#     #     timeslot="9",
#     #     title="아침 기상 및 외출 준비",
#     #     description=(
#     #         "아침에 일어나 에너지 드링크를 마시고 외출할 옷으로 "
#     #         "갈아입은 뒤, 핸드폰과 지갑, 영화 티켓을 가방에 넣는다."
#     #     ),
#     #     outfit="늘어진 면 티셔츠와 편한 트레이닝 팬츠",
#     #     location="강남 오피스텔의 개인 작업실",
#     # )

#     hourly_plan = HourlyPlan(
#         timeslot="9",
#         title="아침 준비 및 홍대 출발 준비",
#         description="알람을 끄고 커피를 내리고, 스마트폰으로 영화 예매 확인 후, 가방에 피자 스낵과 물병을 챙겨 홍대로 나가기 위한 준비를 함",
#         outfit="편안한 캐주얼 티셔츠와 청바지",
#         location="자택",
#     )

#     compiled_graph = build_generate_log_image_graph().compile(
#         checkpointer=InMemorySaver(),
#     )

#     result = await compiled_graph.ainvoke(
#         {
#             "hourly_plan": hourly_plan,
#         },
#         config=create_config("image-subgraph"),
#         context=context,
#         interrupt_before=[
#             "build_final_image_prompt",
#         ],
#     )

#     print("\n//====🧪 Visual prompt reference search query====//")
#     pprint(result.get("visual_prompt_reference_search_query"))

#     assert result.get("visual_prompt_reference_search_query")
#     assert "log_image_url" not in result


@pytest.mark.asyncio
async def test_partial_execution_from_start_query_to_retrieve_image_prompt(
    context: Context,
) -> None:
    compiled_graph = build_generate_log_image_graph().compile(
        checkpointer=InMemorySaver(),
    )

    # hourly_plan = HourlyPlan(
    #     timeslot="9",
    #     title="아침 준비 및 홍대 출발 준비",
    #     description="알람을 끄고 커피를 내리고, 스마트폰으로 영화 예매 확인 후, 가방에 피자 스낵과 물병을 챙겨 홍대로 나가기 위한 준비를 함",
    #     outfit="편안한 캐주얼 티셔츠와 청바지",
    #     location="자택",
    # )

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
        timeslot="15",
        title="홍대 영화관 도착 및 관람 준비",
        description="홍대에 위치한 영화관으로 이동하여 <눈동자> 영화 티켓을 수령하고, 좌석에 앉아 관람 준비를 마침.', outfit='전통 무녀복에 고딕 풍 부츠를 매치한 차림",
        outfit="전통 무녀복에 고딕 풍 부츠를 매치한 차림",
        location="홍대 근처 영화관",
    )

    result = await compiled_graph.ainvoke(
        {
            "hourly_plan": hourly_plan,
        },
        config=create_config("image-subgraph"),
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
