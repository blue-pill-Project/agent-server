from fastapi import APIRouter

from agents.trend_agent.agent import TrendAgent
from api.schemas.trend import TrendResponse


router = APIRouter(prefix="/trend", tags=["trend"])


@router.post("/run", response_model=TrendResponse)
async def run_trend():
    trend_agent = TrendAgent()

    result = await trend_agent.run()

    return TrendResponse(success=result)
