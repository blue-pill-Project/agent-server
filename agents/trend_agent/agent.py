from dataclasses import dataclass
from agents.base import BaseAgent
from agents.trend_agent.graph import build_trend_graph
from common.utils.date import get_current_month


@dataclass
class TrendContext:
    current_month: str


class TrendAgent(BaseAgent):
    def build_graph(self):
        return build_trend_graph()

    async def run(
        self,
    ):
        current_month = get_current_month()

        context = TrendContext(
            current_month=current_month,
        )

        return await self.invoke({}, context=context)
