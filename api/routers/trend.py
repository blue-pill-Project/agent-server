from fastapi import APIRouter, Request
from api.schemas.trend import TrendResponse


router = APIRouter(prefix="/trend", tags=["trend"])


@router.post("/run", response_model=TrendResponse)
async def run_trend(
    request: Request,
):
    trend_agent = request.app.state.trend_agent

    result = await trend_agent.run()

    return TrendResponse(success=result)
