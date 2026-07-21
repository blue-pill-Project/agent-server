from psycopg_pool import AsyncConnectionPool


class DailyPlanRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    def get() -> bool:
        # 구현해야함
        return True

    async def save_all(
        self,
        daily_plans: list[tuple],
    ) -> bool:
        if not daily_plans:
            return True

        query = """
            INSERT INTO daily_plans (
                log_room_id,
                log_room_member_id,
                date,
                day,
                plan
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.executemany(
                        query,
                        daily_plans,
                    )

            return True
        except Exception as e:
            print(f"Failed to save trends: {e}")
            return False
