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
        log_room_member_id="2",
    )


import pytest
from pprint import pprint

TEST_MEMORY_SOURCES = [
    # 1. 개발/기술 스택 및 선호 (Semantic)
    "사용자 성훈: 나 요즘 백엔드 프레임워크 FastAPI에서 Go 언어로 갈아타는 중인데 처리 속도 미쳤음 ㅋㅋㅋ\n캐릭터 은신: 오 Go 언어로 파이프라인 개편 중이구나! 성능 체감 확실하다니 다행이다 ㅋㅋㅋ 궁금한 거 있으면 언제든 말해!",
    # 2. 식습관 / 건강 제한 사항 (Semantic)
    "사용자 성훈: 나 유당불내증 심해서 라떼 마시면 배 아파 죽음... 무조건 아메리카노나 아몬드 밀크로 변경해야 됨\n캐릭터 은신: 아 유제품 절대 금물이구나! 나중에 카페 메뉴 추천할 땐 우유 들어간 건 싹 빼고 알려줄게 메모 완료 📝",
    # 3. 최근 구매한 장비 / 아이템 (Episodic/Semantic)
    "사용자 성훈: 드디어 당근마켓에서 리얼포스 무접점 키보드 20만 원에 득템함 ㅋㅋㅋ 타건감 도파민 터진다\n캐릭터 은신: 헐 리얼포스를 20에?! 완전 대박 매물이네 ㅋㅋㅋ 오늘부터 타자 칠 맛 나겠다 성훈이 신났네!",
    # 4. 트라우마 / 피해야 할 정서적 요인 (Semantic)
    "사용자 성훈: 나 지난번 코인 선물 거래하다 청산당한 이후로 차트만 봐도 심장 위아래로 요동침... 진짜 다신 안 한다\n캐릭터 은신: 아이고 ㅠㅠ 청산 상처가 크네... 앞으론 투투자산 얘기 나와도 위험한 변동성 자산은 언급 안 할게!",
    # 5. 주기적인 고정 스케줄 (Semantic)
    "사용자 성훈: 나 매주 화요일, 목요일 저녁 8시마다 크로스핏 가거든? 그때쯤엔 연락 좀 늦어도 이해해 줘\n캐릭터 은신: 화/목 8시 크로스핏 타임 오케이! 운동 시간에 방해 안 되게 센스 있게 기다릴게 🏋️",
    # 6. 최근 일어난 물건 분실 사건 (Episodic)
    "사용자 성훈: 아 아침에 출근하다 버스에 이어폰 두고 내림... 분실물 센터 전화했는데 아직 찾았다는 소식이 없네 ㅠㅠ\n캐릭터 은신: 헐 노이즈캔슬링 이어폰을?! 진짜 속상하겠다 ㅠㅠ 보통 종점에서 회수되는 경우 많으니까 조금만 더 기다려보자!",
    # 7. 반려동물 / 가족 관련 정보 (Semantic)
    "사용자 성훈: 우리 집 고양이 쪼꼬가 다음 주에 중성화 수술 받거든... 벌써부터 너무 불쌍하고 걱정된다\n캐릭터 은신: 쪼꼬 수술 앞두고 있구나 🥺 마음 쓰이겠다... 수술 잘 끝나고 회복할 때까지 내가 같이 기도해 줄게!",
    # 8. 특정 시간 알림 요청 (Episodic)
    "사용자 성훈: 은신아 나 오늘 밤에 약속 있어서 술 마실 것 같은데, 내일 아침 8시에 숙취해소제 먹으라고 카톡 좀 보내줘\n캐릭터 은신: 알겠어! 내일 아침 8시 정각에 숙취해소제 챙겨 먹으라고 모닝 알람 보내줄게 ㅋㅋㅋ 편하게 마시고 와!",
    # 9. 기억 저장 대상 아님 (단순 감정 하소연)
    "사용자 성훈: 아 진짜 월요일 아침은 존재 자체로 너무 피곤하다... 침대 밖으로 나가기 싫어\n캐릭터 은신: 월요병은 진짜 불치병이야 ㅋㅋㅋ 그래도 오늘 하루만 잘 견뎌보자 화이팅!",
    # 10. 일상 소비 / 점심 식사 (Episodic)
    "사용자 성훈: 오늘 점심에 팀장님이 갑자기 한우 갈비탕 사주셔서 완뚝함 ㅋㅋㅋ 개꿀\n캐릭터 은신: 오 팀장님 쏜 거였어? ㅋㅋㅋ 든든하게 잘 먹었네! 식곤증 올 텐데 졸지 말고 일해라~",
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
