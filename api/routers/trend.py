from fastapi import APIRouter

from agents.trend_agent.agent import TrendAgent
from api.schemas.trend import TrendResponse


router = APIRouter(prefix="/trend", tags=["trend"])

trend_agent = TrendAgent()


@router.post("/run", response_model=TrendResponse)
async def run_trend():

    state = await trend_agent.run()

    return {"is_saved": state["is_saved"]}
