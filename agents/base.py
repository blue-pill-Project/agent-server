from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from psycopg_pool import AsyncConnectionPool


class BaseAgent(ABC):
    def __init__(self, pool: AsyncConnectionPool):
        self._graph: CompiledStateGraph | None = None
        self._pool = pool

    @abstractmethod
    def build_graph(self) -> StateGraph:
        pass

    def get_graph(self) -> CompiledStateGraph:
        if self._graph is None:
            graph_builder = self.build_graph()
            self._graph = graph_builder.compile()

        return self._graph

    async def invoke(
        self, state: dict, config: dict | None = None, context: dict | None = None
    ):
        graph = self.get_graph()
        return await graph.ainvoke(state, config=config, context=context)
