import httpx

from agents.character_chat_agent.tools.phone.services.naver_blog import (
    NaverBlogSearchClient,
)


class EventsService:
    def __init__(
        self,
        blog_client: NaverBlogSearchClient,
    ):
        self._blog_client = blog_client

    async def search(
        self,
        query: str,
        location: str | None = None,
    ) -> str:
        search_query = self._build_query(
            query=query,
            location=location,
        )

        try:
            items = await self._blog_client.search(
                query=search_query,
                display=5,
            )

        except httpx.HTTPError:
            return "행사 정보를 확인하려고 했지만 지금은 검색할 수 없다."

        if not items:
            return (
                f"'{search_query}'와 관련된 "
                "최근 행사 정보를 찾지 못했다. "
                "확인되지 않은 행사를 추측해서 말하지 않는다."
            )

        lines = [
            f"'{search_query}' 관련 최근 행사 언급.",
            (
                "게시글 작성일 기준 검색 결과다. "
                "행사의 실제 진행 여부와 운영시간은 "
                "검색 결과에 명시된 경우에만 확정해서 말한다."
            ),
        ]

        for item in items:
            lines.append(
                f"- [{item['post_date']}] {item['title']} | {item['description']}"
            )

        return "\n".join(lines)

    def _build_query(
        self,
        query: str,
        location: str | None,
    ) -> str:
        parts = []

        if location:
            parts.append(location)

        parts.append(" ".join(query.split()))

        event_keywords = (
            "팝업",
            "전시",
            "공연",
            "축제",
            "행사",
        )

        if not any(keyword in query for keyword in event_keywords):
            parts.append("행사")

        return " ".join(parts)
