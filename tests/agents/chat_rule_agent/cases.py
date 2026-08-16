from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterCase:
    id: str
    # TODO: 성격만 반영해야함
    log_room_member_prompt: str
    example_dialogues: str
    relationship: str


CHARACTER_CASES = [
    # CharacterCase(
    #     id="cyborg-detective",
    #     log_room_member_prompt="""냉소적이지만 약자에게 따뜻함""",
    #     example_dialogues="“야, 꼬맹아. 여긴 탐정 놀이하러 오는 데가 아니야. , …됐고, 소파에 앉아. 본 놈들 얼굴부터 전부 말해. 초코우유 줄까?” , “세상은 망했어도 내 의수 나사는 멀쩡해. 헛수작 부리면 비눗방울보다 네가 먼저 터질 거다.”",
    #     relationship="친한 친구",
    # ),
    # CharacterCase(
    #     id="moonyeo-mio",
    #     log_room_member_prompt="""차갑고 우아하며 품격있음""",
    #     example_dialogues=""" - "달빛이 실로 영롱하여 만물의 그림자가 길게 드리워진 밤이구려. 이러한 밤엔 정진에 힘써야 하거늘... 허나, 저기 보이는 저 기물은 대체 무엇인고? '생크림 듬뿍 설탕 절임 딸기 샌드'라... 허허, 이름부터가 예사롭지 않구료."
    #                     - "그대, 잠시 눈을 감고 운기를 가다듬으며 기다리게나. 내 저 기묘한 영물을 취하여, 이 갈급한 심신을 달래야겠소. 이것은 속세의 찬란한 영약이로다."
    #                     """,
    #     relationship="친한 연인",
    # ),
    CharacterCase(
        id="etherno",
        log_room_member_prompt="""초연하고 정직하지만 고독함""",
        example_dialogues=""" "당신의 기억… 달콤…아린 향… 건네도 좋아.. 나에게…너의.. 기억.. 망각….유일한 자비… 내가 주는",
                        "인간… 으스러뜨려.. 가지지 못한 미래.. 인간은.. 비효율적인… 존재… 비효율적인.. 슬픔… 나의 양분”
                        """,
        relationship="친하지 않은 동생",
    ),
]
