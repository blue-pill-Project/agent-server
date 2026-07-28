from dataclasses import dataclass
from agents.base import BaseAgent
from agents.weekly_plan_agent.graph import build_weekly_plan_graph
from agents.weekly_plan_agent.state import Context
from common.utils.datetime import create_week_dates, get_current_date, get_current_month, get_next_week_start
from domains.daily_plan.repository import DailyPlanRepository
from domains.log_room_member.repository import LogRoomMemberRepository
from domains.trend.repository import TrendRepository


class WeeklyPlanAgent(BaseAgent):
    def __init__(
        self,
        trend_repository: TrendRepository,
        daily_plan_repository: DailyPlanRepository,
        log_room_member_repository: LogRoomMemberRepository,
    ):
        super().__init__()

        self._trend_repository = trend_repository
        self._daily_plan_repository = daily_plan_repository
        self._log_room_member_repository = log_room_member_repository

    def build_graph(self):
        return build_weekly_plan_graph()

    async def run(self, user_id: str, log_room_id: str, log_room_member_id: str):

        current_month = get_current_month()
        current_date = get_current_date()
        week_start = get_next_week_start(current_date)   # 다가오는 주 월요일
        week_dates = create_week_dates(week_start)
        log_room_member_prompt = await self._log_room_member_repository.get_prompt(
            user_id, log_room_id, log_room_member_id
        )
        trends = await self._trend_repository.get_by_month(current_month)

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

        success = await self._daily_plan_repository.save_all(rows)

        return success
