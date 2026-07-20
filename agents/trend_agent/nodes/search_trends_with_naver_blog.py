import os
import urllib.request
import urllib.parse
import json
from dotenv import load_dotenv
from agents.trend_agent.state import GraphState
from langgraph.runtime import Runtime
from agents.trend_agent.state import Context

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


def search_trends_with_naver_blog(state: GraphState, runtime: Runtime[Context]) -> dict:
    """
    검색어 5개를 네이버 블로그 검색 API로 조회하고,
    검색어당 10개씩 총 50개 raw 데이터를 raw_blog_datas에 저장하는 노드.
    """
    current_month = runtime.context.current_month

    search_words = [
        "서울 팝업스토어",
        "영화",
        "편의점 신상",
    ]

    raw_trend_results_with_naver_blog = []

    for search_word in search_words:
        enc_text = urllib.parse.quote(str(current_month) + " " + search_word)

        url = (
            "https://openapi.naver.com/v1/search/blog"
            f"?query={enc_text}&display=10&sort=sim"
        )

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
        request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)

        response = urllib.request.urlopen(request)

        response_body = response.read()
        result = json.loads(response_body.decode("utf-8"))

        raw_trend_results_with_naver_blog.append(result.get("items", []))

    return {"raw_trend_results_with_naver_blog": raw_trend_results_with_naver_blog}
