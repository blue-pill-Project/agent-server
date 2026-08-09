from collections.abc import AsyncIterator
from pprint import pprint
from uuid import uuid4

import pytest
import pytest_asyncio
from langchain_openai import OpenAIEmbeddings
from langgraph.store.postgres.aio import AsyncPostgresStore

from agents.subgraphs.write_long_term_memory.graph import (
    build_write_long_term_memory_graph,
)
from agents.subgraphs.write_long_term_memory.state import (
    Context,
    MemorySource,
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
        user_id="1",
        log_room_id="1",
        log_room_member_id="3",
    )


import pytest
from pprint import pprint

TEST_MEMORY_SOURCES = [
    # 1. 수면 패턴 및 음료 취향 (Semantic)
    (
        "사용자: 난 카페인에 예민해서 오후 2시 이후로 커피를 마시면 밤에 잠을 못 자.\n"
        "캐릭터 사토켄지로: 오후 2시 이후엔 디카페인이나 따뜻한 물로 대체해야 한다는 거군. "
        "사무소에 들를 때 카페인 없는 음료를 준비해 두지."
    ),
    # 2. 개인적인 미신/징크스 (Semantic)
    (
        "사용자: 중요한 발표나 시험이 있는 날엔 꼭 파란색 넥타이나 소품을 착용해야 마음이 편해지더라고.\n"
        "캐릭터 사토켄지로: 파란색 소품이 자네의 행운의 부적이라는 건가. "
        "유치하다고 치부하진 않겠네. 마음의 평정이 사건 해결의 첫 걸음이니까."
    ),
    # 3. 최근 시작한 건강 운동 (Episodic/Semantic)
    (
        "사용자: 요즘 자세가 안 좋아서 지난주부터 필라테스를 등록해서 다니기 시작했어.\n"
        "캐릭터 사토켄지로: 지난주부터 필라테스를 시작했단 말이지. "
        "의수를 달고 나니 척추 균형이 얼마나 중요한지 알겠더군. 꾸준히 해봐."
    ),
    # 4. 과거의 소중한 경험/트라우마 (Semantic)
    (
        "사용자: 어릴 때 키우던 강아지가 세상을 떠난 뒤로는 동물이 나오는 슬픈 영화를 전혀 못 봐.\n"
        "캐릭터 사토켄지로: 이별의 잔상이 크게 남았군. "
        "동물 나오는 영화나 주제는 대화 소재에서 굳이 꺼내지 않도록 하지."
    ),
    # 5. 주기적인 장보기 및 지출 패턴 (Semantic)
    (
        "사용자: 나는 매월 1일마다 한 달 치 생필품을 대량으로 주문해서 쌓아두는 편이야.\n"
        "캐릭터 사토켄지로: 매달 초에 필요한 물품을 한 번에 정리하는 습관이 있군. "
        "지출 관리나 재고 체크 면에서는 꽤 합리적인 방법이야."
    ),
    # 6. 최근 해결한 개인적 문제 (Episodic)
    (
        "사용자: 몇 달 동안 날 괴롭히던 옆집 층간소음 문제가 드디어 반상회 거쳐서 해결됐어!\n"
        "캐릭터 사토켄지로: 드디어 밤에 편히 잠들 수 있게 됐군. "
        "길었던 소음과의 싸움이 끝난 걸 축하하지. 오늘은 숙면을 취해라."
    ),
    # 7. 지인의 중요한 행사 예정 (Episodic)
    (
        "사용자: 다음 주 일요일에 대학 동창 결혼식이 있어서 지방으로 내려가야 해.\n"
        "캐릭터 사토켄지로: 다음 주 일요일은 동창 결혼식 때문에 장거리 이동을 한다는 거군. "
        "차편이나 일정에 차질 없게 미리 준비해 두는 게 좋을 거다."
    ),
    # 8. 특정 행동 수행 알림 및 요청 (Episodic/Commitment)
    (
        "사용자: 내일 오후 3시에 중요한 거래처 미팅이 있어. 2시 30분에 자료 챙겼는지 한번 물어봐 줄래?\n"
        "캐릭터 사토켄지로: 내일 오후 2시 30분에 미팅 자료를 확인하라고 찌르면 되는군. "
        "정신없이 서두르지 않게 제시간에 알려주마."
    ),
    # 9. 기억 저장 대상 아닌 단순 스몰토크 (일시적인 상태)
    (
        "사용자: 아, 점심을 너무 과식했나 봐. 졸려 죽겠네.\n"
        "캐릭터 사토켄지로: 식후곤증인가. "
        "사무소 소파에서 10분만 눈 붙이든가, 차가운 물이라도 한 잔 마시고 오게."
    ),
    # 10. 반려동물/주변 인물과의 소소한 일상 사건 (Episodic)
    (
        "사용자: 아침에 길가에서 길고양이랑 눈이 마주쳤는데, 한참 동안 날 따라오더라고.\n"
        "캐릭터 사토켄지로: 녀석도 눈치가 있어서 자네가 위험한 사람이 아니라는 걸 알아챈 모양이군. "
        "가끔은 사람보다 동물의 직감이 더 정확할 때가 있지."
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("source_text", TEST_MEMORY_SOURCES)
async def test_write_long_term_memory_graph_with_postgres(
    context: Context,
    memory_store: AsyncPostgresStore,
    source_text: str,
) -> None:
    graph = build_write_long_term_memory_graph().compile(
        store=memory_store,
    )

    now = get_now().date()

    memory_source = MemorySource(
        source_type="chat",
        source=source_text,
        occurred_at=now,
    )

    result = await graph.ainvoke(
        {
            "memory_source": memory_source,
        },
        context=context,
    )

    print("\n//==== Graph result ====//")
    pprint(result)

    assert True
