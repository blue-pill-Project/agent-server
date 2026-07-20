from fastapi import APIRouter

from agents.weekly_plan_agent.agent import WeeklyPlanAgent
from api.schemas.weekly_plan import WeeklyPlanRequest, WeeklyPlanResponse

router = APIRouter(prefix="/weekly-plan", tags=["weekly_plan"])

@router.post("/run", response_model=WeeklyPlanResponse)
async def run_weekly_plan(
    request: WeeklyPlanRequest,
):
    weekly_plan_agent = WeeklyPlanAgent()
    user_id = request.user_id
    log_room_id = request.log_room_id
    log_room_member_id = request.log_room_member_id

    result = await weekly_plan_agent.run(user_id, log_room_id, log_room_member_id)

    return WeeklyPlanResponse(success=result)
