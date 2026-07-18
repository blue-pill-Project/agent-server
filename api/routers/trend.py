from fastapi import APIRouter

from api.schemas.trend import TrendResponse
from agents.trend_agent.graph import build_trend_graph
from common.utils.date import get_current_month


router = APIRouter(
    prefix="/trend",
    tags=["trend"]
)

trend_graph = build_trend_graph()
compiled_trend_graph = trend_graph.compile()


@router.post(
    "/run",
    response_model=TrendResponse
)
async def run_trend():

    current_month = get_current_month()

    state = compiled_trend_graph.invoke(
        {
            "current_month": current_month
        }
    )

    return {
        "is_saved": state["is_saved"]
    }