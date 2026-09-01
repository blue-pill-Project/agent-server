from datetime import datetime
from typing import Any
from psycopg_pool import AsyncConnectionPool


class MessageRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def find_recent_messages(
        self,
        log_room_id: int,
        reference_time: datetime,
        hours: int = 24,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        query = """
            SELECT *
            FROM (
                SELECT
                    chat_message_id,
                    sender_id,
                    content,
                    created_at
                FROM chat_messages
                WHERE log_room_id = %s
                  AND created_at >= %s - (%s * INTERVAL '1 hour')
                ORDER BY created_at DESC
                LIMIT %s
            ) AS recent_messages
            ORDER BY created_at ASC
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (
                        log_room_id,
                        reference_time,
                        hours,
                        limit,
                    ),
                )

                rows = await cursor.fetchall()

        return [dict(row) for row in rows]
