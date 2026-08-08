from collections.abc import AsyncIterator
from pprint import pprint
import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.subgraphs.search_long_term_memory.graph import (
    build_search_long_term_memory_graph,
)
from agents.subgraphs.search_long_term_memory.state import (
    Context,
    Source,
)
from common.config import settings
from common.utils.datetime import get_now


@pytest_asyncio.fixture
async def memory_store() -> AsyncIterator[AsyncPostgresStore]:
    embeddings = OpenAIEmbeddings(
        model="openai/text-embedding-3-small",
        api_key=settings.OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    async with AsyncPostgresStore.from_conn_string(
        settings.DATABASE_URL,
        index={
            "embed": embeddings,
            "dims": 1536,
            "fields": ["content"],
        },
    ) as store:
        await store.setup()

        yield store


@pytest.fixture
def context() -> Context:
    return Context(
        user_id="1", log_room_id="1", log_room_member_id="2", now=get_now().date()
    )


TEST_CHAT_SOURCES = [
    # "쪼꼬가 많이 아프네...ㅠㅠ",
    # "하 내 버킷리스트를 이룰수있을까?",
    # "안녕?",
    # "나 지금 너무 높이 올라왔어 무섭네",
    # "오늘 진짜 힘드네",
    "오늘 어디갈까 추천해줘",
]


# @pytest.mark.asyncio
# @pytest.mark.parametrize("source_text", TEST_CHAT_SOURCES)
# async def test_search_long_term_memory_graph_with_chat(
#     context: Context,
#     memory_store: AsyncPostgresStore,
#     source_text: str,
# ) -> None:
#     graph = build_search_long_term_memory_graph().compile(
#         store=memory_store,
#     )

#     source = Source(
#         purpose="chat",
#         source=source_text,
#     )

#     result = await graph.ainvoke(
#         {
#             "source": source,
#         },
#         context=context,
#     )

#     print("\n//==== Graph result ====//")
#     pprint(result)

#     assert True


TEST_SOURCES = [
    # Source(
    #     purpose="post",
    #     source="""[Target Timeslot]
    # 18:00-21:00 (timeslot=18)
    # [Daily Plan]
    # 오전과 오후에는 집에서 웹툰 마감 작업을 한다.
    # 저녁에는 크로스핏 센터에서 운동한다.
    # 운동이 끝나면 집으로 돌아와 저녁을 먹고 휴식한다.
    # [Previous Hourly Plans]
    # 09:00-12:00 - 아침을 먹고 웹툰 콘티 작업을 시작한다.
    # 12:00-15:00 - 점심을 먹고 작화 작업을 이어간다.
    # 15:00-18:00 - 작업을 마무리하고 크로스핏에 갈 준비를 한다.""",
    # ),
    # Source(
    #     purpose="chat",
    #     source="나 지금 너무 높이 올라왔어 무섭네",
    # ),
    # Source(
    #     purpose="chat",
    #     source="쪼꼬가 많이 아프네...ㅠㅠ",
    # ),
    Source(
        purpose="post",
        source="""
    [Target Timeslot]
    06:00-09:00 (timeslot=06)
    [Daily Plan]
    새로나온 신상 디저트 구매 예정
    [Previous Hourly Plans]
    없음
    """,
    ),
    #     # 2. 성수동 데이트 중 다음 일정
    #     """
    # [Target Timeslot]
    # 15:00-18:00 (timeslot=15)
    # [Daily Plan]
    # 사용자와 캐릭터가 성수동에서 하루 동안 데이트한다.
    # 점심을 먹고 전시와 팝업스토어를 구경한 뒤 카페에 들른다.
    # 저녁에는 근처 식당에서 함께 식사한다.
    # [Previous Hourly Plans]
    # 09:00-12:00 - 외출 준비를 마치고 성수동으로 이동한다.
    # 12:00-15:00 - 사용자와 만나 점심을 먹고 전시를 관람한다.
    # """.strip(),
    #     # 3. 병원 예약처럼 활동이 확정된 계획
    #     """
    # [Target Timeslot]
    # 15:00-18:00 (timeslot=15)
    # [Daily Plan]
    # 오후 4시에 병원 진료 예약이 있다.
    # 진료가 끝나면 약국에 들른 뒤 바로 집으로 돌아간다.
    # [Previous Hourly Plans]
    # 09:00-12:00 - 집에서 쉬면서 병원에 가져갈 서류를 확인한다.
    # 12:00-15:00 - 점심을 먹고 병원에 갈 준비를 한다.
    # """.strip(),
    #     # 4. 집에서 웹툰 마감 작업
    #     """
    # [Target Timeslot]
    # 21:00-24:00 (timeslot=21)
    # [Daily Plan]
    # 오늘은 집에서 웹툰 마감 작업을 진행한다.
    # 저녁까지 주요 작업을 끝내고 밤에는 남은 부분을 정리한 뒤 휴식한다.
    # [Previous Hourly Plans]
    # 12:00-15:00 - 점심을 먹고 웹툰 작화 작업을 진행한다.
    # 15:00-18:00 - 집중해서 주요 장면의 채색을 마무리한다.
    # 18:00-21:00 - 저녁을 먹고 수정해야 할 원고를 확인한다.
    # """.strip(),
    #     # 5. 집 정리와 저녁 휴식
    #     """
    # [Target Timeslot]
    # 18:00-21:00 (timeslot=18)
    # [Daily Plan]
    # 주말을 맞아 미뤄둔 방 정리를 한다.
    # 오전에는 세탁과 청소를 하고 오후에는 책상과 작업 공간을 정리한다.
    # 저녁에는 집에서 편안하게 쉬며 좋아하는 콘텐츠를 본다.
    # [Previous Hourly Plans]
    # 09:00-12:00 - 밀린 세탁을 하고 방 안을 청소한다.
    # 12:00-15:00 - 점심을 먹고 잠시 휴식한다.
    # 15:00-18:00 - 책상과 작업 도구를 정리하고 쓰레기를 버린다.
    # """.strip(),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("source_text", TEST_SOURCES)
async def test_search_long_term_memory_graph(
    context: Context,
    memory_store: AsyncPostgresStore,
    source_text: str,
) -> None:
    graph = build_search_long_term_memory_graph().compile(
        store=memory_store,
    )

    source = source_text

    result = await graph.ainvoke(
        {
            "source": source,
        },
        context=context,
    )

    print("\n//==== Graph result ====//")
    pprint(result)

    assert True
