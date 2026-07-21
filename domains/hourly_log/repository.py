from psycopg_pool import AsyncConnectionPool


class HourlyLogRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def save(
        self,
        hourly_log: tuple,
    ) -> bool:
        if not hourly_log:
            return True

        query = """
            INSERT INTO log_photos
                (public_id, log_room_member_id, post_date, time_slot,
                    image_url, caption, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (log_room_member_id, post_date, time_slot)
            DO UPDATE SET image_url  = EXCLUDED.image_url,
                            caption    = EXCLUDED.caption,
                            updated_at = EXCLUDED.updated_at
        """

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(
                        query,
                        hourly_log,
                    )

            return True
        except Exception as e:
            print(f"Failed to save trends: {e}")
            return False
