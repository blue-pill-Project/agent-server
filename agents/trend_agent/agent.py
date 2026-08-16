from agents.base import BaseAgent
from agents.trend_agent.graph import build_trend_graph
from agents.trend_agent.state import Context
from common.utils.datetime import get_current_month
from domains.trend.repository import TrendRepository


class TrendAgent(BaseAgent):
    def __init__(
        self,
        trend_repository: TrendRepository,
    ):
        super().__init__()

        self._trend_repository = trend_repository

    def build_graph(self):
        return build_trend_graph()

    async def run(
        self,
    ):
        current_month = get_current_month()

        context = Context(
            current_month=current_month,
        )

        state = await self.invoke({}, context=context)

        trends = state["trends"]

        rows = [
            (current_month, t.title, t.category, t.location, t.summary)
            for t in trends.trends
        ]

        success = await self._trend_repository.save_all(rows)

        return success
