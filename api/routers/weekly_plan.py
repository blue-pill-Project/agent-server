from fastapi import APIRouter, Request
from api.schemas.weekly_plan import WeeklyPlanRequest, WeeklyPlanResponse

router = APIRouter(prefix="/weekly-plan", tags=["weekly_plan"])


@router.post("/run", response_model=WeeklyPlanResponse)
async def run_weekly_plan(
    body: WeeklyPlanRequest,
    request: Request,
):
    weekly_plan_agent = request.app.state.weekly_plan_agent
    user_id = body.user_id
    log_room_id = body.log_room_id
    log_room_member_id = body.log_room_member_id

    result = await weekly_plan_agent.run(user_id, log_room_id, log_room_member_id)

    return WeeklyPlanResponse(success=result)
