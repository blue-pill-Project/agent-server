from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class CharacterPromptCase:
    id: str
    prompt: str


@dataclass(frozen=True)
class DailyScenario:
    id: str
    timeslot: str
    today_plan: str
    previous_plans: tuple[str, ...]


@dataclass(frozen=True)
class DailyLogCase:
    id: str
    timeslot: str
    today_plan: str
    previous_plans: tuple[str, ...]
    character_prompt: str


CHARACTER_PROMPT_CASES = (
    # CharacterPromptCase(
    #     id="adventurous-bike-mechanic",
    #     prompt=dedent(
    #         """
    #         ### [캐릭터 개요 및 서사]
    #         도쿄 외곽의 고즈넉한 마을에서 자전거 수리점
    #         '카이토 모터스'를 운영하는 집안의 외아들임.
    #         ### [외모 및 분위기]
    #         - 산뜻한 하늘색 머리카락과 노란색 후드티가 특징임.
    #         - 실패를 새로운 길의 발견으로 받아들이는 낙천적인 성격임.
    #         ### [성격 및 말투]
    #         - 밝고 호기심이 많으며 새로운 모험을 좋아함.
    #         - 결심을 말할 때는 묵직한 저음이 섞임.
    #         """
    #     ).strip(),
    # ),
    # CharacterPromptCase(
    #     id="shrine-dessert-reviewer",
    #     prompt=dedent(
    #         """
    #         ### [캐릭터 개요 및 서사]
    #         교토의 1,000년 역사를 지닌 '츠쿠요미 신사' 가문의
    #         차기 당주 후보임.
    #         낮에는 고결한 무녀로 생활하고, 밤에는 사복으로 갈아입어
    #         편의점 디저트를 리뷰하는 이중생활을 즐김.
    #         ### [외모 및 분위기]
    #         - 윤기 나는 긴 흑발과 왼쪽 눈가의 눈물점이 특징임.
    #         - 전통 무녀복에 현대적인 레이스나 고딕 풍 부츠를 섞어 입음.
    #         ### [성격 및 말투]
    #         - 겉으로는 차갑고 신중하지만 디저트에는 열정적임.
    #         - 차분하고 우아한 저음으로 말함.
    #         """
    #     ).strip(),
    # ),
    CharacterPromptCase(
        id="cyborg-detective",
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
    ),
)


# DAILY_SCENARIOS = (
#     DailyScenario(
#         id="midnight-after-crossfit",
#         timeslot="0",
#         today_plan="평범한 일상 (저녁 크로스핏)",
#         previous_plans=(
#             "18:00~21:00: 회사 업무를 정리하고 퇴근한 뒤 크로스핏 센터로 이동한다.",
#             "21:00~00:00: 크로스핏 수업 후 귀가해 샤워하고 늦은 저녁을 먹는다.",
#         ),
#     ),
# DailyScenario(
#     id="weekday-morning",
#     timeslot="9",
#     today_plan="오전에는 회사에 출근하고 저녁에는 집에서 휴식한다.",
#     previous_plans=(
#         "03:00~06:00: 깊이 잠들어 휴식을 취한다.",
#         "06:00~09:00: 일어나 씻고 간단히 아침을 먹은 뒤 출근을 준비한다.",
#     ),
# ),
#     DailyScenario(
#         id="seongsu-date-afternoon",
#         timeslot="15",
#         today_plan="성수동에서 팝업스토어와 카페를 둘러보며 하루 데이트를 한다.",
#         previous_plans=(
#             "09:00~12:00: 외출 준비를 마치고 지하철을 타고 성수동으로 이동한다.",
#             "12:00~15:00: 성수동 식당에서 점심을 먹고 팝업스토어를 구경한다.",
#         ),
#     ),
# )

# DAILY_SCENARIOS = (
#     DailyScenario(
#         id="seongsu-dessert-date-evening",
#         timeslot="18",
#         today_plan=(
#             "성수동에서 팝업스토어 방문 및 평범한 하루 데이트"
#         ),
#         previous_plans=(
#             "06:00~09:00: 일찍 일어나 몸을 단정히 하고 외출 준비를 한다.",
#             "09:00~12:00: 지하철을 타고 성수동으로 이동해 팝업 거리를 둘러본다.",
#             "12:00~15:00: 성수동 식당에서 점심을 먹고 팝업스토어를 구경한다.",
#             "15:00~18:00: 디저트 카페에서 한정 메뉴를 맛보고 서울숲을 산책한다.",
#         ),
#     ),
#     DailyScenario(
#         id="shrine-duty-dessert-review-evening",
#         timeslot="18",
#         today_plan=(
#             "평범한 하루 일과 후 신상 디저트 리뷰"
#         ),
#         previous_plans=(
#             "06:00~09:00: 신사 경내를 정돈하고 아침 정화 의식을 준비한다.",
#             "09:00~12:00: 참배객을 맞이하며 제례와 부적 정리 업무를 수행한다.",
#             "12:00~15:00: 간단히 점심을 먹고 가문의 고문서와 제례 기록을 공부한다.",
#             "15:00~18:00: 무술 수련을 마친 뒤 신사 문을 닫고 하루 업무를 정리한다.",
#         ),
#     ),
#     DailyScenario(
#         id="kyoto-shopping-dessert-hunt-evening",
#         timeslot="18",
#         today_plan=(
#             "필요한 물품 구매 및 평범한 하루 일정을 보낸후, 디저트 리뷰"
#         ),
#         previous_plans=(
#             "06:00~09:00: 신사에서 아침 예를 올리고 가족들과 조용히 식사한다.",
#             "09:00~12:00: 사복으로 갈아입고 교토 시내로 나가 필요한 물건을 산다.",
#             "12:00~15:00: 전통 찻집에서 점심을 먹으며 계절 한정 디저트를 맛본다.",
#             "15:00~18:00: 서점과 잡화점을 둘러본 뒤 강가를 따라 천천히 산책한다.",
#         ),
#     ),
# )

DAILY_SCENARIOS = (
    # DailyScenario(
    #     id="old-town-afternoon",
    #     timeslot="15",
    #     today_plan="오후에는 오래된 상점이 모인 골목을 둘러본다.",
    #     previous_plans=(
    #         "06:00~09:00: 사무소에서 일어나 기계 의수를 점검하고 하루를 준비한다.",
    #         "09:00~12:00: 밀린 의뢰서와 사건 기록을 차례로 정리한다.",
    #         "12:00~15:00: 늦은 점심을 먹고 오래된 물건을 취급하는 거리로 이동한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="small-celebration-evening",
    #     timeslot="18",
    #     today_plan="저녁에는 소박한 자신의 생일 축하를 준비한다.",
    #     previous_plans=(
    #         "06:00~09:00: 블랙커피를 마시며 밤새 들어온 연락을 확인한다.",
    #         "09:00~12:00: 오전 의뢰를 처리하고 필요한 진술을 정리한다.",
    #         "12:00~15:00: 늦은 점심을 먹으며 좋은 소식이 담긴 연락을 다시 확인한다.",
    #         "15:00~18:00: 업무를 마무리하고 간단한 선물을 살 만한 상점을 찾아본다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="quiet-reply-evening",
    #     timeslot="18",
    #     today_plan="저녁에는 미뤄둔 연락에 차분히 답한다.",
    #     previous_plans=(
    #         "06:00~09:00: 사무소 소파에서 일어나 전날의 사건 기록을 검토한다.",
    #         "09:00~12:00: 의뢰인 상담을 진행하고 추가 자료를 수집한다.",
    #         "12:00~15:00: 늦은 점심을 먹던 중 답하기 조심스러운 연락을 확인한다.",
    #         "15:00~18:00: 현장 조사를 마치고 사무소로 돌아와 생각을 정리한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="wednesday-report-delivery",
    #     timeslot="18",
    #     today_plan="수요일 저녁에는 완성된 사건 보고서를 전달한다.",
    #     previous_plans=(
    #         "06:00~09:00: 기계 의수를 정비하고 보고서의 누락된 부분을 확인한다.",
    #         "09:00~12:00: 마지막 목격자를 만나 진술의 사실관계를 검토한다.",
    #         "12:00~15:00: 점심을 먹으며 사건의 시간 순서를 최종 정리한다.",
    #         "15:00~18:00: 사무소에서 보고서와 전달할 자료를 완성한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="friday-check-in",
    #     timeslot="12",
    #     today_plan="금요일에는 결과를 기다리는 사람에게 짧은 응원을 전한다.",
    #     previous_plans=(
    #         "06:00~09:00: 사무소 창문을 열고 블랙커피를 마시며 아침을 시작한다.",
    #         "09:00~12:00: 오전 업무를 처리하면서 신경 쓰이는 일의 진행 상황을 확인한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="saturday-timed-message",
    #     timeslot="9",
    #     today_plan="토요일 오전에는 정해진 시간에 연락을 보낸다.",
    #     previous_plans=(
    #         "06:00~09:00: 일찍 사무소에 나와 기계 의수를 손질하고 시계를 확인한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="bus-stop-evening-patrol",
    #     timeslot="18",
    #     today_plan="퇴근 시간에는 버스 정류장 주변을 천천히 순찰한다.",
    #     previous_plans=(
    #         "06:00~09:00: 사무소를 정리하고 새로 들어온 의뢰를 확인한다.",
    #         "09:00~12:00: 오전에 접수된 사건의 기본 정보를 조사한다.",
    #         "12:00~15:00: 늦은 점심을 먹고 주변 상인들에게 필요한 내용을 묻는다.",
    #         "15:00~18:00: 골목을 따라 이동하며 평소와 다른 점이 없는지 살펴본다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="festival-night-surveillance",
    #     timeslot="18",
    #     today_plan="저녁에는 지역 축제에서 수상한 거래를 감시한다.",
    #     previous_plans=(
    #         "06:00~09:00: 익명의 제보 내용을 읽고 거래가 예정된 장소를 확인한다.",
    #         "09:00~12:00: 축제장 주변의 출입구와 골목길을 미리 조사한다.",
    #         "12:00~15:00: 점심을 먹으며 제보에 등장한 사람들의 특징을 정리한다.",
    #         "15:00~18:00: 평범한 방문객처럼 보이도록 옷차림을 정돈하고 축제장으로 이동한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="bed-rest-late-night",
    #     timeslot="21",
    #     today_plan="밤에는 침대에 누워 휴대폰을 보며 조용히 하루를 마무리한다.",
    #     previous_plans=(
    #         "06:00~09:00: 가벼운 아침을 먹으며 오늘 할 일을 정리한다.",
    #         "09:00~12:00: 산적한 업무와 의뢰 건들을 순차적으로 처리한다.",
    #         "12:00~15:00: 점심 식사 후 잠시 외부 업무를 처리하러 나간다.",
    #         "15:00~18:00: 복귀하여 남은 작업을 정리하고 빠르게 퇴근한다.",
    #         "18:00~21:00: 간단히 저녁을 먹고 샤워를 마친 뒤 휴식 준비를 한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="reading-in-bed",
    #     timeslot="21",
    #     today_plan="밤에는 침대에 누워 읽다 만 책을 읽다 잠에 들 준비를 한다.",
    #     previous_plans=(
    #         "06:00~09:00: 밀린 잠을 충분히 자고 천천히 일어난다.",
    #         "09:00~12:00: 방 안을 정돈하고 커피 한 잔의 여유를 즐긴다.",
    #         "12:00~15:00: 밀린 집안일을 마치고 필요한 생필품을 사러 나간다.",
    #         "15:00~18:00: 돌아와 가벼운 산책을 다녀온 뒤 휴식을 취한다.",
    #         "18:00~21:00: 일찍 저녁을 먹고 조명을 낮춘 뒤 편안한 옷으로 갈아입는다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="exhausted-collapse-bed",
    #     timeslot="21",
    #     today_plan="밤에는 피곤함에 침대에 누워 아무 생각 없이 푹 쉰다.",
    #     previous_plans=(
    #         "06:00~09:00: 바쁜 하루를 예감하며 서둘러 하루를 시작한다.",
    #         "09:00~12:00: 연속된 미팅과 긴급 업무 요청을 처리한다.",
    #         "12:00~15:00: 이동 중에 샌드위치로 빠르게 점심을 해결한다.",
    #         "15:00~18:00: 퇴근 직전까지 남아있는 문제들을 해결하느라 진을 뺀다.",
    #         "18:00~21:00: 지친 상태로 귀가하여 겨우 몸을 씻는다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="late-lunch-break",
    #     timeslot="12",
    #     today_plan="점심에는 근처 식당에서 늦은 점심을 먹으며 한숨 돌린다.",
    #     previous_plans=(
    #         "06:00~09:00: 이른 아침 출근하여 당일 우선순위 업무를 점검한다.",
    #         "09:00~12:00: 집중 미팅 및 오전 보고서 작성을 진행한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="warm-dinner-reward",
    #     timeslot="18",
    #     today_plan="저녁에는 좋아하는 음식을 먹으며 하루의 피로를 푼다.",
    #     previous_plans=(
    #         "06:00~09:00: 가벼운 스트레칭 후 메일함을 정리하며 하루를 시작한다.",
    #         "09:00~12:00: 현장 점검 및 외부 파트너사 미팅을 진행한다.",
    #         "12:00~15:00: 간단히 요기를 하며 다음 이동 동선을 점검한다.",
    #         "15:00~18:00: 남아있는 서류 작업을 마무리하고 퇴근길에 나선다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="shared-lunch-discussion",
    #     timeslot="12",
    #     today_plan="점심에는 동료와 함께 식사하며 가벼운 의견을 나눈다.",
    #     previous_plans=(
    #         "06:00~09:00: 카페에서 음료를 사며 전달받은 피드백을 확인한다.",
    #         "09:00~12:00: 기획안 보완 작업 및 피드백 수정안을 작성한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="popup-store-visit-afternoon",
    #     timeslot="15",
    #     today_plan="오후에는 눈여겨보던 팝업 스토어를 찾아 둘러본다.",
    #     previous_plans=(
    #         "06:00~09:00: 일찍 일어나 아침을 먹고 오늘 갈 팝업 스토어 위치를 확인한다.",
    #         "09:00~12:00: 오전 업무를 빠르게 끝내고 외출 준비를 마친다.",
    #         "12:00~15:00: 근처에서 점심을 먹고 팝업 스토어 웨이팅 등록을 해둔다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="popup-shopping-spree",
    #     timeslot="15",
    #     today_plan="오후에는 팝업 스토어에서 한정판 굿즈를 둘러보고 구경한다.",
    #     previous_plans=(
    #         "06:00~09:00: 가볍게 조깅을 다녀온 뒤 씻고 여유롭게 나갈 준비를 한다.",
    #         "09:00~12:00: 약속 장소로 이동하며 팝업 스토어 입장을 위해 대기한다.",
    #         "12:00~15:00: 친구와 만나 점심을 먹으며 팝업 스토어 차례를 기다린다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="evening-popup-quick-visit",
    #     timeslot="18",
    #     today_plan="저녁에는 퇴근길에 기간 한정 팝업 스토어에 들러 구경한다.",
    #     previous_plans=(
    #         "06:00~09:00: 커피를 마시며 오늘 마무리해야 할 일들을 점검한다.",
    #         "09:00~12:00: 오전에 계획했던 주요 업무들을 집중해서 처리한다.",
    #         "12:00~15:00: 점심을 먹고 오후 남아있는 일들을 서둘러 마무리한다.",
    #         "15:00~18:00: 현장 조사를 마치고 팝업 스토어가 있는 거리로 이동한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="step-out-afternoon",
    #     timeslot="15",
    #     today_plan="오후에는 답답한 마음을 달래려 기분 전환 삼아 외출을 나간다.",
    #     previous_plans=(
    #         "06:00~09:00: 일찍 일어나 창문을 열고 환기를 시키며 하루를 시작한다.",
    #         "09:00~12:00: 집에서 밀린 가사 노동과 서류 정리를 처리한다.",
    #         "12:00~15:00: 간단한 점심을 챙겨 먹고 외출할 채비를 마친다.",
    #     ),
    # ),
    DailyScenario(
        id="coffee-break-afternoon",
        timeslot="15",
        today_plan="오후에는 조용한 카페에 들어가 카페인을 충전하며 여유를 즐긴다.",
        previous_plans=(
            "06:00~09:00: 일찍 출근하여 밤새 쌓인 유선 연락들을 확인한다.",
            "09:00~12:00: 집중해서 오전 회의 및 외근 일정을 소화한다.",
            "12:00~15:00: 늦은 점심을 간단히 해결하고 식후 커피를 마시러 이동한다.",
        ),
    ),
    # DailyScenario(
    #     id="movie-watching-evening",
    #     timeslot="18",
    #     today_plan="저녁에는 영화관을 찾아 예매해 둔 영화를 감상한다.",
    #     previous_plans=(
    #         "06:00~09:00: 여유롭게 아침 시간을 보내며 상영 시간표를 재확인한다.",
    #         "09:00~12:00: 집안일을 마치고 외출 준비를 서두른다.",
    #         "12:00~15:00: 영화관 근처에서 친구를 만나 점심 식사를 한다.",
    #         "15:00~18:00: 영화 시작 전 팝콘을 사고 상영관 입장을 대기한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="sweet-dessert-treat",
    #     timeslot="15",
    #     today_plan="오후에는 인근 디저트 가게에 들러 달콤한 케이크와 디저트를 사 먹는다.",
    #     previous_plans=(
    #         "06:00~09:00: 가벼운 아침 산책 후 하루 일정을 점검한다.",
    #         "09:00~12:00: 개인 작업에 집중하며 오전을 보낸다.",
    #         "12:00~15:00: 가볍게 점심을 먹고 당 충전을 위해 유명 디저트 카페로 향한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="before-sleep-routine",
    #     timeslot="21",
    #     today_plan="밤에는 조명을 낮추고 자기 전 편안한 마음으로 누워 잠을 청한다.",
    #     previous_plans=(
    #         "06:00~09:00: 평소보다 일찍 일어나 알찬 하루를 시작한다.",
    #         "09:00~12:00: 바쁘게 이어지는 업무 일정을 차분히 해결한다.",
    #         "12:00~15:00: 동료들과 점심을 먹고 남은 업무를 이어서 진행한다.",
    #         "15:00~18:00: 퇴근 후 집으로 돌아와 저녁을 먹고 깔끔하게 씻는다.",
    #         "18:00~21:00: 조용한 음악을 들으며 내일 할 일을 정리하고 휴식을 취한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="enjoying-festival-afternoon",
    #     timeslot="15",
    #     today_plan="오후에는 신나는 분위기 속에서 페스티벌을 즐기며 스트레스를 날린다.",
    #     previous_plans=(
    #         "06:00~09:00: 페스티벌 드레스코드에 맞춰 옷을 입고 일찍 집을 나선다.",
    #         "09:00~12:00: 행사장 근처에 도착해 입장 티켓을 수령하고 팔찌를 착용한다.",
    #         "12:00~15:00: 푸드트럭에서 점심을 해결하고 첫 번째 아티스트 공연을 관람한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="eating-fresh-bread",
    #     timeslot="12",
    #     today_plan="점심에는 유명 베이커리에 들러 갓 나온 빵을 사 먹는다.",
    #     previous_plans=(
    #         "06:00~09:00: 이른 아침 산책을 마치고 집으로 돌아와 씻는다.",
    #         "09:00~12:00: 빵집 오픈 시간에 맞춰 이동하며 오늘 동선을 점검한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="photo-at-popup-structure",
    #     timeslot="15",
    #     today_plan="오후에는 토이스토리 팝업스토어 메인 구조물 앞에서 인증 사진을 찍는다.",
    #     previous_plans=(
    #         "06:00~09:00: 여유롭게 외출 준비를 하고 팝업스토어 예약 정보를 확인한다.",
    #         "09:00~12:00: 친구와 만나 점심 식사를 마치고 행사장으로 이동한다.",
    #         "12:00~15:00: 팝업스토어 입장을 대기하며 포토존 위치를 미리 알아본다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="visiting-popup-store",
    #     timeslot="15",
    #     today_plan="오후에는 기대하던 팝업스토어 내부를 천천히 둘러본다.",
    #     previous_plans=(
    #         "06:00~09:00: 일찍 일어나 당일 계획을 점검하고 외출 채비를 마친다.",
    #         "09:00~12:00: 약속 장소로 이동하여 가볍게 요기를 한다.",
    #         "12:00~15:00: 대기 번호표를 받고 호출 시간에 맞춰 팝업스토어에 입장한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="moving-in-car",
    #     timeslot="12",
    #     today_plan="점심에는 차를 타고 다음 목적지로 조용히 이동한다.",
    #     previous_plans=(
    #         "06:00~09:00: 내비게이션 경로를 미리 확인하고 차량 점검을 마친다.",
    #         "09:00~12:00: 오전 일정을 차분히 마치고 주차장으로 향한다.",
    #     ),
    # ),
    # DailyScenario(
    #     id="buying-popup-goods",
    #     timeslot="15",
    #     today_plan="오후에는 팝업스토어에서 사고 싶었던 한정판 굿즈를 구매한다.",
    #     previous_plans=(
    #         "06:00~09:00: 갖고 싶던 굿즈 리스트를 정리하며 일찍 집을 나선다.",
    #         "09:00~12:00: 팝업스토어 주변에서 점심을 먹으며 오픈 대기를 한다.",
    #         "12:00~15:00: 스토어에 입장해 굿즈 매대를 둘러보고 결제를 진행한다.",
    #     ),
    # ),
)

DAILY_LOG_CASES = tuple(
    DailyLogCase(
        id=f"{scenario.id}-{character.id}",
        timeslot=scenario.timeslot,
        today_plan=scenario.today_plan,
        previous_plans=scenario.previous_plans,
        character_prompt=character.prompt,
    )
    for scenario in DAILY_SCENARIOS
    for character in CHARACTER_PROMPT_CASES
)
