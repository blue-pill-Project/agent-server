from langgraph.store.base import (
    BaseStore,
)


class LongTermMemoryRepository:
    def __init__(
        self,
        store: BaseStore,
    ):
        self._store = store

    async def add(
        self,
        namespace: tuple[str, ...],
        memory_key: str,
        memory: dict,
    ) -> None:
        await self._store.aput(
            namespace,
            memory_key,
            memory.model_dump(mode="json"),
        )
