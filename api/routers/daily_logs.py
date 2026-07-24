from fastapi import APIRouter, Request
from api.schemas.daily_logs import DailyLogsRequest, DailyLogsResponse

router = APIRouter(prefix="/daily-logs", tags=["daily_logs"])


@router.post("/run", response_model=DailyLogsResponse)
async def run_daily_logs(
    body: DailyLogsRequest,
    request: Request,
):
    daily_logs_agent = request.app.state.daily_logs_agent

    timeslot = body.timeslot
    user_id = body.user_id
    log_room_id = body.log_room_id
    log_room_member_id = body.log_room_member_id
    previous_plans = body.previous_plans

    result = await daily_logs_agent.run(
        timeslot, user_id, log_room_id, log_room_member_id, previous_plans
    )

    return DailyLogsResponse(success=result)
