import logging
from typing import Literal

from langchain_core.tools import tool

from common.config import settings

from agents.character_chat_agent.tools.phone.services import (
    EventsService,
    NaverBlogSearchClient,
    SocialService,
)


logger = logging.getLogger(__name__)


PhoneAction = Literal[
    "social",
    "events",
]

naver_blog_client = NaverBlogSearchClient(
    client_id=settings.NAVER_CLIENT_ID,
    client_secret=settings.NAVER_CLIENT_SECRET,
)


social_service = SocialService(
    blog_client=naver_blog_client,
)


events_service = EventsService(
    blog_client=naver_blog_client,
)


@tool
async def use_phone(
    action: PhoneAction,
    query: str,
    location: str | None = None,
) -> str:
    """
    캐릭터가 스마트폰으로 현재 외부 정보를 확인할 때 사용한다.

    action:
    - social: 최근 온라인 유행, 화제, 신상품
    - events: 최근 행사, 팝업, 전시, 공연, 축제

    social 사용 규칙:
    - query는 검색엔진에 넣을 짧은 검색어로 작성한다.
    - 2~5개 정도의 핵심 키워드만 사용한다.
    - 비슷한 의미의 단어를 길게 나열하지 않는다.
    - location과 같은 지역명을 query에 중복하지 않는다.

    social 좋은 예:
    - query="편의점 신상"
    - query="편의점 인기 간식"
    - query="여름 패션 유행"

    social 나쁜 예:
    - query="최근 편의점 인기 상품 유행 먹거리 신상 한국 GS25 CU 세븐일레븐"

    events 사용 규칙:
    - query에는 찾고 싶은 행사 종류나 조건을 짧게 넣는다.
    - location이 있다면 지역명은 location에 넣는다.

    events 좋은 예:
    - query="주말 팝업", location="성수"
    - query="캐릭터 전시", location="홍대"
    """

    logger.info(
        "use_phone 호출 | action=%s | query=%s | location=%s",
        action,
        query,
        location,
    )

    match action:
        case "social":
            result = await social_service.search(
                query=query,
                location=location,
            )

        case "events":
            result = await events_service.search(
                query=query,
                location=location,
            )

        case _:
            raise ValueError(f"지원하지 않는 phone action입니다: {action}")

    logger.debug(
        "use_phone 결과 | %s",
        result,
    )

    return result
