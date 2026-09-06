from psycopg_pool import AsyncConnectionPool


class LogRoomMemberRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def get_info(
        self,
        log_room_member_id: int,
    ) -> dict | None:
        query = """
            SELECT cs.name, cs.description, cs.prompt, cs.example_dialogues
            FROM log_room_members lrm
            JOIN character_snapshots cs ON cs.snapshot_id = lrm.snapshot_id
            WHERE lrm.log_room_member_id = %s
            LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (log_room_member_id,),
                )

                row = await cursor.fetchone()

        if not row:
            return None

        return {
            "name": row["name"],
            "description": row["description"],
            "prompt": row["prompt"],
            "example_dialogues": row["example_dialogues"],
        }

    async def get_character_image_key(
        self,
        log_room_member_id: int,
    ) -> str | None:
        query = """
            SELECT cs.image_url
            FROM log_room_members lrm
            JOIN character_snapshots cs ON cs.snapshot_id = lrm.snapshot_id
            WHERE lrm.log_room_member_id = %s
            LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (log_room_member_id,))
                row = await cursor.fetchone()

        return row["image_url"] if row else None

    # TODO: Logroom Repositiry로 분리해야할듯
    async def get_relationship(
        self,
        log_room_id: int,
    ) -> dict | None:
        query = """
                SELECT label
                FROM log_room_relationships
                WHERE log_room_id = %s
                LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (log_room_id,),
                )
                row = await cursor.fetchone()

        if not row:
            return None

        return row["label"] if row else "친구"
