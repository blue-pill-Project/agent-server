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


def get_now():
    return datetime.now(ZoneInfo("Asia/Seoul"))


def get_current_date():
    return date.today()


def get_current_month():
    return date.today().replace(day=1)


def add_days(target_date: date, days: int) -> date:
    return target_date + timedelta(days=days)


def get_next_week_start(current_date: date) -> date:
    """다가오는 주의 월요일. (일요일에 실행하면 내일 월요일, 이미 월요일이면 다음 주 월요일)"""
    days_until_monday = (7 - current_date.weekday()) % 7   # Mon=0..Sun=6
    days_until_monday = days_until_monday or 7             # 오늘이 월요일이면 다음 주로
    return current_date + timedelta(days=days_until_monday)


def create_week_dates(start_date: date) -> list[dict]:
    return [
        {
            "date": start_date + timedelta(days=i),
            "weekday": WEEKDAYS[(start_date + timedelta(days=i)).weekday()],
        }
        for i in range(7)
    ]
