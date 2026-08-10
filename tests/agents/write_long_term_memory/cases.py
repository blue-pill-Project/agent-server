from dataclasses import dataclass
import datetime
from typing import Literal

from common.utils.datetime import get_now


now = get_now().date()


@dataclass(frozen=True)
class WriteLongTermCase:
    id: str
    source: str
    occurred_at: datetime.date
    source_type: Literal["chat", "post"] | None = None


WRITE_LONG_TERM_CASES = [
    # 1. 수면 패턴 및 음료 취향 (Semantic)
    WriteLongTermCase(
        id="sleep_with_coffee",
        source_type="chat",
        source="사용자: 난 카페인에 예민해서 오후 2시 이후로 커피를 마시면 밤에 잠을 못 자.\n"
        "캐릭터 사토켄지로: 오후 2시 이후엔 디카페인이나 따뜻한 물로 대체해야 한다는 거군. "
        "사무소에 들를 때 카페인 없는 음료를 준비해 두지.",
        occurred_at=now,
    )
]
