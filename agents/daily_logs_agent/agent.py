from uuid import uuid4
from agents.base import BaseAgent
from agents.daily_logs_agent.graph import build_daily_logs_graph
from agents.daily_logs_agent.state import Context
from common.utils.date import get_current_date, get_current_month, get_now
from domains.daily_plan.repository import DailyPlanRepository
from domains.hourly_log.repository import HourlyLogRepository
from domains.log_room_member.repository import LogRoomMemberRepository
from langgraph.graph.state import BaseStore


class DailyLogsAgent(BaseAgent):
    def __init__(
        self,
        log_room_member_repository: LogRoomMemberRepository,
        daily_plan_repository: DailyPlanRepository,
        hourly_log_repository: HourlyLogRepository,
        store: BaseStore,
    ):
        super().__init__(
            store=store,
        )

        self._log_room_member_repository = log_room_member_repository
        self._daily_plan_repository = daily_plan_repository
        self._hourly_log_repository = hourly_log_repository

    def build_graph(self):
        return build_daily_logs_graph()

    async def run(
        self,
        timeslot: str,
        user_id: str,
        log_room_id: str,
        log_room_member_id: str,
        previous_plans: list,
    ):

        current_month = get_current_month()
        current_date = get_current_date()
        now = get_now()
        log_room_member_prompt = await self._log_room_member_repository.get_prompt(
            user_id, log_room_id, log_room_member_id
        )
        today_plan = await self._daily_plan_repository.get_today(
            log_room_id, log_room_member_id, current_date
        )

        context = Context(
            user_id=user_id,
            log_room_id=log_room_id,
            log_room_member_id=log_room_member_id,
            current_month=current_month,
            current_date=current_date,
            timeslot=timeslot,
            previous_plans=previous_plans,
            log_room_member_prompt=log_room_member_prompt,
            today_plan=today_plan,
            # NOTE:잠깐 이미지 하드코딩
            image_url="https://i.pinimg.com/736x/91/5e/0e/915e0e09e60665b3b653b7f8d7a30113.jpg",
        )

        state = await self.invoke({}, context=context)

        hourly_log = state["hourly_log"]

        hourly_log_for_save = (
            uuid4(),
            log_room_member_id,
            current_date,
            hourly_log.timeslot,
            hourly_log.log_image_url,
            hourly_log.log_text.log_text,
            now,
            now,
        )

        success = await self._hourly_log_repository.save(hourly_log_for_save)

        return success
