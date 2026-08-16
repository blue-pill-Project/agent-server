from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class SearchLongTermCase:
    id: str
    purpose: Literal["chat", "post"]
    source: str


SEARCH_LONG_TERM_CASES = [
    SearchLongTermCase(
        id="greeting",
        purpose="chat",
        source="안녕? 오늘 하루는 어땠어?",
    ),
    SearchLongTermCase(
        id="favorite-food",
        purpose="chat",
        source="나 제일 좋아하는 음식이 뭔지 맞춰볼래?",
    ),
    SearchLongTermCase(
        id="funny-story",
        purpose="chat",
        source="심심한데 재미있는 이야기 하나만 해줘.",
    ),
    SearchLongTermCase(
        id="song-recommendation",
        purpose="chat",
        source="지금 날씨랑 어울리는 노래 하나 추천해줄 수 있어?",
    ),
    SearchLongTermCase(
        id="character-favorite-movie",
        purpose="chat",
        source="너는 어떤 영화를 제일 좋아해?",
    ),
    SearchLongTermCase(
        id="restaurant-recommendation",
        purpose="chat",
        source="혹시 맛집 추천받을 수 있을까?",
    ),
    SearchLongTermCase(
        id="coffee-preference",
        purpose="chat",
        source="갑자기 너무 졸려... 커피 마실까?",
    ),
    SearchLongTermCase(
        id="character-dream",
        purpose="chat",
        source="너의 꿈은 뭐야?",
    ),
    SearchLongTermCase(
        id="emotional-support",
        purpose="chat",
        source="나 오늘 진짜 힘든 일이 있었어, 들어줄래?",
    ),
    SearchLongTermCase(
        id="current-feeling",
        purpose="chat",
        source="지금 내 기분은 '설렘'인데, 너는 어때?",
    ),
    SearchLongTermCase(
        id="rainy-day-food",
        purpose="chat",
        source="비 오는 날엔 역시 파전이지 않니?",
    ),
    SearchLongTermCase(
        id="future-travel",
        purpose="chat",
        source="나중에 우리 같이 여행 가면 어디가 제일 좋을까?",
    ),
]
