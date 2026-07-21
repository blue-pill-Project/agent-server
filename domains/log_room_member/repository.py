from psycopg_pool import AsyncConnectionPool


class LogRoomMemberRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def get_prompt(
        self,
        user_id: int,
        log_room_id: int,
        log_room_member_id: int,
    ) -> dict | None:
        query =  """
            SELECT cs.name, cs.description, cs.prompt
            FROM log_room_members lrm
            JOIN character_snapshots cs ON cs.snapshot_id = lrm.snapshot_id
            WHERE lrm.log_room_member_id = %s
            LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (
                        log_room_member_id,
                        # log_room_id,
                    ),
                )

                row = await cursor.fetchone()

        if not row:
            return None
        
        return {
            "name": row["name"],
            "description": row["description"],
            "prompt": row["prompt"],
        }

