from agents.base import BaseAgent
from agents.trend_agent.graph import build_trend_graph
from agents.trend_agent.state import Context
from common.utils.date import get_current_month
from domains.trend.repository import save_trends


class TrendAgent(BaseAgent):
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

        success = save_trends(state["trends"], current_month)

        return success
