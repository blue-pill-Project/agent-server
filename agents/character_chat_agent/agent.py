from agents.base import BaseAgent
from agents.character_chat_agent.graph import build_character_chat_graph
from agents.character_chat_agent.state import Context
from common.utils.datetime import get_current_date, get_now
from common.utils.reranker import BgeReranker
from domains.log_room_member.repository import LogRoomMemberRepository
from langgraph.graph.state import BaseStore
from langgraph.checkpoint.base import BaseCheckpointSaver


class CharacterChatAgent(BaseAgent):
    def __init__(
        self,
        log_room_member_repository: LogRoomMemberRepository,
        store: BaseStore,
        checkpointer: BaseCheckpointSaver,
        reranker: BgeReranker,
    ):
        super().__init__(
            store=store,
            checkpointer=checkpointer,
        )
        self._reranker = reranker
        self._log_room_member_repository = log_room_member_repository

    def build_graph(self):
        return build_character_chat_graph()

    async def run(
        self, user_id: str, log_room_id: str, log_room_member_id: str, content: str
    ):
        current_date = get_current_date()
        now = get_now()
        thread_id = (
            f"room_{log_room_id}:character_{log_room_member_id}:user_{user_id}:test"
        )
        log_room_member_info = await self._log_room_member_repository.get_info(
            log_room_member_id
        )
        log_room_relationships = (
            await self._log_room_member_repository.get_relationship(log_room_id)
        )

        context = Context(
            user_id=user_id,
            log_room_id=log_room_id,
            log_room_member_id=log_room_member_id,
            current_date=current_date,
            now=now,
            log_room_member_info=log_room_member_info,
            log_room_relationships=log_room_relationships,
            reranker=self._reranker,
        )

        state = await self.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": content,
                    }
                ],
            },
            config={
                "configurable": {
                    "thread_id": thread_id,
                }
            },
            context=context,
        )

        last_message = state["messages"][-1]

        reply = (
            last_message.content
            if hasattr(last_message, "content")
            else last_message["content"]
        )

        return reply
