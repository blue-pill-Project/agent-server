import html
import re

import httpx


NAVER_BLOG_SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json"


class NaverBlogSearchClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        client: httpx.AsyncClient | None = None,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._client = client

    async def search(
        self,
        query: str,
        display: int = 5,
    ) -> list[dict]:
        if self._client:
            return await self._search(
                client=self._client,
                query=query,
                display=display,
            )

        async with httpx.AsyncClient(
            timeout=10.0,
        ) as client:
            return await self._search(
                client=client,
                query=query,
                display=display,
            )

    async def _search(
        self,
        client: httpx.AsyncClient,
        query: str,
        display: int,
    ) -> list[dict]:
        response = await client.get(
            NAVER_BLOG_SEARCH_URL,
            headers={
                "X-Naver-Client-Id": self._client_id,
                "X-Naver-Client-Secret": self._client_secret,
            },
            params={
                "query": query,
                "display": display,
                "start": 1,
                "sort": "date",
            },
        )

        response.raise_for_status()

        items = response.json().get(
            "items",
            [],
        )

        return [
            {
                "title": clean_html(item.get("title", "")),
                "description": clean_html(item.get("description", "")),
                "blogger_name": clean_html(item.get("bloggername", "")),
                "post_date": format_post_date(item.get("postdate", "")),
                "link": item.get("link", ""),
            }
            for item in items
        ]


def clean_html(
    value: str,
) -> str:
    value = re.sub(
        r"<[^>]+>",
        "",
        value,
    )

    return html.unescape(value).strip()


def format_post_date(
    value: str,
) -> str:
    if len(value) != 8:
        return value

    return f"{value[:4]}-{value[4:6]}-{value[6:8]}"
