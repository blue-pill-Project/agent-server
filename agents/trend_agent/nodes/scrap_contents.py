import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from agents.trend_agent.state import GraphState


def convert_naver_blog_url(url: str) -> str:
    """
    Naver 블로그 URL을 변환합니다.
    https://blog.naver.com/{blog_id}/{log_no}
    → https://blog.naver.com/PostView.naver?blogId={blog_id}&logNo={log_no}
    """
    parsed = urlparse(url)

    if parsed.netloc != "blog.naver.com":
        return url

    parts = parsed.path.strip("/").split("/")

    if len(parts) >= 2:
        blog_id = parts[0]
        log_no = parts[1]
        return f"https://blog.naver.com/PostView.naver?blogId={blog_id}&logNo={log_no}"

    return url


def scrap_contents(state: GraphState) -> dict:
    """
    선별된 블로그 내용을 스크래핑하여 본문 텍스트만 scraped_contents에 저장하는 노드.
    """

    filtered_results = state["filtered_results"]
    blogs = filtered_results.filtered_results

    scraped_contents = []

    for blog_data in blogs:
        link = blog_data.link
        print(link)

        converted_url = convert_naver_blog_url(link)

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://blog.naver.com/",
        }

        try:
            response = requests.get(converted_url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.HTTPError:
            print(f"Skip {converted_url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        content_candidates = [
            soup.select_one("div.se-main-container"),
            soup.select_one("#postViewArea"),
            soup.select_one("div#post-view"),
        ]

        content_text = ""

        for candidate in content_candidates:
            if candidate:
                content_text = candidate.get_text(separator="\n", strip=True)
                break

        if not content_text:
            content_text = soup.get_text(separator="\n", strip=True)

        scraped_contents.append(content_text[:8000])

    return {"scraped_contents": scraped_contents}
