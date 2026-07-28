from datetime import date, timedelta, datetime
from zoneinfo import ZoneInfo

WEEKDAYS = [
    "월요일",
    "화요일",
    "수요일",
    "목요일",
    "금요일",
    "토요일",
    "일요일",
]

TIMESLOT_LABELS = {
    0: "자정부터 새벽 3시까지",
    3: "새벽 3시부터 오전 6시까지",
    6: "오전 6시부터 오전 9시까지",
    9: "오전 9시부터 정오까지",
    12: "정오부터 오후 3시까지",
    15: "오후 3시부터 오후 6시까지",
    18: "오후 6시부터 오후 9시까지",
    21: "오후 9시부터 자정까지",
}


def get_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))


def get_current_date():
    return date.today()


def get_current_month():
    return date.today().replace(day=1)


def add_days(target_date: date, days: int) -> date:
    return target_date + timedelta(days=days)


def create_week_dates(start_date: date) -> list[dict]:
    return [
        {
            "date": start_date + timedelta(days=i),
            "weekday": WEEKDAYS[(start_date + timedelta(days=i)).weekday()],
        }
        for i in range(7)
    ]


def get_timeslot_label(timeslot: int) -> str:
    try:
        return TIMESLOT_LABELS[timeslot]
    except KeyError:
        raise ValueError(f"지원하지 않는 시간대입니다: {timeslot}")
