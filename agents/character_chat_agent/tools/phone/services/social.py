import httpx

from agents.character_chat_agent.tools.phone.services.naver_blog import (
    NaverBlogSearchClient,
)


IGNORED_LOCATIONS = {
    "한국",
    "대한민국",
    "South Korea",
}


class SocialService:
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
            return (
                "최근 온라인 정보를 확인하려고 했지만 "
                "지금은 검색할 수 없다. "
                "최신 정보를 추측해서 말하지 않는다."
            )

        if not items:
            return (
                f"'{search_query}' 검색 결과가 없다. "
                "현재 확인된 최신 정보가 없으므로 "
                "구체적인 상품이나 유행을 추측해서 말하지 않는다."
            )

        lines = [f"'{search_query}' 관련 최근 온라인 언급:"]

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
        query = " ".join(query.split()).strip()

        if location and location not in IGNORED_LOCATIONS:
            return f"{location} {query}"

        return query
