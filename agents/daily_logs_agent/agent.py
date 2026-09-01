import logging
from uuid import uuid4
from agents.base import BaseAgent
from agents.daily_logs_agent.graph import build_daily_logs_graph
from agents.daily_logs_agent.state import Context
from common.utils.datetime import (
    get_current_date,
    get_current_month,
    get_now,
    get_timeslot_label,
)
from common.utils.reranker import BgeReranker
from domains.daily_plan.repository import DailyPlanRepository
from domains.hourly_log.repository import HourlyLogRepository
from domains.hourly_plan.repository import HourlyPlanRepository
from domains.log_room_member.repository import LogRoomMemberRepository
from domains.visual_prompt_reference.repository import VisualPromptReferenceRepository
from common.config import settings
from langgraph.graph.state import BaseStore

logger = logging.getLogger(__name__)


class DailyLogsAgent(BaseAgent):
    def __init__(
        self,
        log_room_member_repository: LogRoomMemberRepository,
        daily_plan_repository: DailyPlanRepository,
        hourly_log_repository: HourlyLogRepository,
        hourly_plan_repository: HourlyPlanRepository,
        visual_prompt_reference_repository: VisualPromptReferenceRepository,
        store: BaseStore,
        reranker: BgeReranker,
    ):
        super().__init__(
            store=store,
        )
        self._reranker = reranker
        self._log_room_member_repository = log_room_member_repository
        self._daily_plan_repository = daily_plan_repository
        self._hourly_log_repository = hourly_log_repository
        self._hourly_plan_repository = hourly_plan_repository
        self._visual_prompt_reference_repository = visual_prompt_reference_repository

    def build_graph(self):
        return build_daily_logs_graph()

    async def run(
        self,
        timeslot: str,
        user_id: str,
        log_room_id: str,
        log_room_member_id: str,
    ):
        logger.info(
            "daily logs 시작 | room=%s | member=%s | timeslot=%s",
            log_room_id,
            log_room_member_id,
            timeslot,
        )
        now = get_now()
        current_month = get_current_month()
        current_date = get_current_date()
        timeslot_label = get_timeslot_label(int(timeslot))
        now = get_now()
        log_room_member_prompt = await self._log_room_member_repository.get_prompt(
            user_id, log_room_id, log_room_member_id
        )
        today_plan = await self._daily_plan_repository.get_today(
            log_room_id, log_room_member_id, current_date
        )
        # daily_plan 은 있으면 연결. 없어도(주간 계획 미생성) 로그·hourly_plan 은 생성한다.
        daily_plan_id = today_plan["daily_plan_id"] if today_plan else None
        # NOTE: 이전 계획 불러오기 current_date 의 오전 6시 이후
        previous_plans = await self._hourly_plan_repository.get_by_today_after_six(log_room_member_id)
        recent_messages = await self._message_repository.find_recent_messages(
            log_room_id=log_room_id,
            reference_time=now,
            hours=24,
            limit=20,
        )
        # 캐릭터 참조 이미지 (R2 공개 URL). 없으면 참조 없이 진행.
        image_key = await self._log_room_member_repository.get_character_image_key(
            log_room_member_id
        )
        if image_key:
            image_url = f"{settings.R2_PUBLIC_DOMAIN}/{image_key}"
        else:
            image_url = None
            print(
                f"캐릭터 참조 이미지 없음 - 참조 없이 생성: member={log_room_member_id}"
            )

        context = Context(
            user_id=user_id,
            log_room_id=log_room_id,
            log_room_member_id=log_room_member_id,
            now=now,
            current_month=current_month,
            current_date=current_date,
            timeslot=timeslot,
            timeslot_label=timeslot_label,
            previous_plans=previous_plans,
            log_room_member_prompt=log_room_member_prompt,
            today_plan=today_plan,
            image_url=image_url,
            visual_prompt_reference_repository=(
                self._visual_prompt_reference_repository
            ),
            reranker=self._reranker,
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

        log_saved = await self._hourly_log_repository.save(hourly_log_for_save)

        hourly_plan = hourly_log.hourly_plan
        plan_saved = await self._hourly_plan_repository.save(
            (
                daily_plan_id,
                log_room_member_id,
                current_date,
                int(hourly_plan.timeslot),
                hourly_plan.title,
                hourly_plan.description,
                hourly_plan.outfit,
                hourly_plan.location,
            )
        )

        success = log_saved and plan_saved

        logger.info(
            "daily logs 저장 완료 | member=%s | log_saved=%s | plan_saved=%s",
            log_room_member_id,
            log_saved,
            plan_saved,
        )

        return success
