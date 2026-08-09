from fastapi import APIRouter, Request

from api.schemas.log_rooms import LogRoomDeleteResponse

router = APIRouter(prefix="/log-rooms", tags=["log_rooms"])


async def _delete_checkpoints(pool, checkpointer, log_room_id: str) -> None:
    """방에 속한 모든 대화 thread 의 체크포인트 삭제."""
    prefix = f"room_{log_room_id}:%"
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT DISTINCT thread_id FROM checkpoints WHERE thread_id LIKE %s",
                (prefix,),
            )
            rows = await cur.fetchall()

    for row in rows:
        await checkpointer.adelete_thread(row["thread_id"])


async def _delete_memories(store, log_room_id: str) -> None:
    """방에 속한 장기기억(store) 삭제."""
    prefix = ("memories", str(log_room_id))
    while True:
        items = await store.asearch(prefix, limit=100)
        if not items:
            break
        for item in items:
            await store.adelete(item.namespace, item.key)


@router.delete("/{log_room_id}", response_model=LogRoomDeleteResponse)
async def delete_log_room(log_room_id: str, request: Request):
    pool = request.app.state.db_pool
    store = request.app.state.store
    checkpointer = request.app.state.checkpointer
    daily_plan_repository = request.app.state.daily_plan_repository

    await daily_plan_repository.delete_by_room(log_room_id)
    await _delete_checkpoints(pool, checkpointer, log_room_id)
    await _delete_memories(store, log_room_id)

    return LogRoomDeleteResponse(success=True)
