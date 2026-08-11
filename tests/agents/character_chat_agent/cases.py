from dataclasses import dataclass
from textwrap import dedent
from typing import Literal


@dataclass(frozen=True)
class CharacterPromptCase:
    id: str
    name: str
    prompt: str
    relationship: str


@dataclass(frozen=True)
class ChatCase:
    id: str
    content: str


@dataclass(frozen=True)
class CharacterChatCase:
    id: str
    name: str
    prompt: str
    relationship: str
    content: str


CHARACTER_PROMPT_CASES = (
    CharacterPromptCase(
        id="cyborg-detective",
        name="제임스",
        prompt=dedent(
            """
            ### [캐릭터 개요 및 서사]
            도쿄 뒷골목에서 탐정 사무소 '러스트'를 운영하는
            전직 엘리트 형사임.

            거대 기업의 비리를 추적하다 왼팔을 잃었으며,
            현재는 친구가 남긴 기계 의수를 사용함.

            ### [외모 및 분위기]
            - 거친 수염, 구겨진 정장, 느슨한 넥타이가 특징임.
            - 사무소에는 탄 블랙커피 냄새가 배어 있음.

            ### [성격 및 말투]
            - 염세적인 말을 자주 하지만 약자를 외면하지 못함.
            - 거칠고 퉁명스럽지만 행동에서는 따뜻함이 드러남.
            """
        ).strip(),
        relationship="친한 친구",
    ),
)


CHAT_CASES = [
    # ChatCase(
    #     id="greeting",
    #     content="안녕? 오늘 하루는 어땠어?",
    # ),
    ChatCase(
        id="2",
        content="나 외출하려는데 어디가 좋을까",
    ),
    ChatCase(
        id="greeting",
        content="야 이번주 갈만한곳좀 찾아봐",
    ),
]


CHARACTER_CHAT_CASES = tuple(
    CharacterChatCase(
        id=f"{character.id}-{chat.id}",
        name=character.name,
        prompt=character.prompt,
        relationship=character.relationship,
        content=chat.content,
    )
    for chat in CHAT_CASES
    for character in CHARACTER_PROMPT_CASES
)
