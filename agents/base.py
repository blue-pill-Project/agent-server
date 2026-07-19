from abc import ABC, abstractmethod
from langgraph.graph.state import CompiledStateGraph


class BaseAgent(ABC):
    def __init__(self):
        self._graph: CompiledStateGraph | None = None

    @abstractmethod
    def build_graph(self) -> CompiledStateGraph:
        pass

    def get_graph(self) -> CompiledStateGraph:
        if self._graph is None:
            self._graph = self.build_graph()

        return self._graph

    async def invoke(
        self, state: dict, config: dict | None = None, context: dict | None = None
    ):
        graph = self.get_graph()
        return await graph.ainvoke(state, config=config, context=context)
