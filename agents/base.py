from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langgraph.graph.state import BaseStore, CompiledStateGraph


class BaseAgent(ABC):
    def __init__(
        self,
        # store: BaseStore | None = None,
        # checkpointer : BaseCheckpointer
    ):
        self._graph: CompiledStateGraph | None = None
        # self._store = store
        # self._checkpointer = store

    @abstractmethod
    def build_graph(self) -> StateGraph:
        pass

    def get_graph(self) -> CompiledStateGraph:
        if self._graph is None:
            graph_builder = self.build_graph()
            self._graph = graph_builder.compile(
                # store=self._store,
                # checkpointer=self._checkpointer
            )

        return self._graph

    async def invoke(
        self, state: dict, config: dict | None = None, context: dict | None = None
    ):
        graph = self.get_graph()
        return await graph.ainvoke(state, config=config, context=context)
