from dataclasses import dataclass

from psycopg_pool import AsyncConnectionPool
from agents.base import BaseAgent
from agents.weekly_plan_agent.graph import build_weekly_plan_graph
from agents.weekly_plan_agent.state import Context
from common.utils.date import create_week_dates, get_current_date, get_current_month
from domains.daily_plan.repository import save_daily_plans
from domains.log_room_member.repository import get_log_room_member_prompt
from domains.trend.repository import get_trends


@dataclass
class WeeklyPlanContext:
    current_month: str
    current_date: str
    week_dates: list[dict]
    log_room_member_prompt: dict
    trends: list[dict]


class WeeklyPlanAgent(BaseAgent):
    def __init__(self, pool: AsyncConnectionPool):
        super().__init__(pool)

    def build_graph(self):
        return build_weekly_plan_graph()

    async def run(self, user_id: str, log_room_id: str, log_room_member_id: str):

        current_month = get_current_month()
        current_date = get_current_date()
        week_dates = create_week_dates(current_date)
        log_room_member_prompt = get_log_room_member_prompt(
            user_id, log_room_id, log_room_member_id
        )
        trends = await get_trends(current_month, self._pool)

        context = Context(
            user_id=user_id,
            log_room_id=log_room_id,
            log_room_member_id=log_room_member_id,
            current_month=current_month,
            current_date=current_date,
            week_dates=week_dates,
            log_room_member_prompt=log_room_member_prompt,
            trends=trends,
        )

        state = await self.invoke({}, context=context)

        plans = state["weekly_plan"]

        rows = [
            (
                log_room_id,
                log_room_member_id,
                day_info["date"],
                day_info["weekday"],
                plan.plan,
            )
            for day_info, plan in zip(
                week_dates,
                plans.daily_plans,
            )
        ]

        success = save_daily_plans(rows)

        return success
