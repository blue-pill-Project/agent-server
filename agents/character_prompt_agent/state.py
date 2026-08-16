from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


@dataclass
class Context:
    name: str
    intro: str
    user_prompt: str


class CharacterPrompt(BaseModel):
    """완성된 캐릭터 프롬프트"""

    name: str = Field(description="캐릭터 이름. 입력된 이름을 그대로 사용")
    age: int = Field(description="캐릭터에 어울리는 나이(숫자)")
    job: str = Field(description="캐릭터의 직업")
    personality: str = Field(
        description="성격을 간단하게. 예: '소심한 성격이다', '대인관계가 어렵다'. 30자 이내"
    )
    background: str = Field(
        description=(
            "어린시절과 현재 목표/추구하는 것을 담은 배경. "
            "예: '할렘가에서 살아왔고 지금은 돈을 버는 게 목적이다'. 100자 이내"
        )
    )


class GraphState(TypedDict):
    character_prompt: CharacterPrompt
