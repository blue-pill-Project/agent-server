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


def create_week_dates(start_date: date) -> list[dict]:
    return [
        {
            "date": start_date + timedelta(days=i),
            "weekday": WEEKDAYS[(start_date + timedelta(days=i)).weekday()],
        }
        for i in range(7)
    ]
