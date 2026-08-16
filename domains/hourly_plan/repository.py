from psycopg_pool import AsyncConnectionPool


class HourlyPlanRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def save(self, row: tuple) -> bool:
        """hourly_plan 저장.
        (daily_plan_id, timeslot) 유니크라 재실행 시 덮어쓴다.
        """
        query = """
            INSERT INTO hourly_plans (
                daily_plan_id, timeslot, title, description, outfit, location
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (daily_plan_id, timeslot) DO UPDATE SET
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                outfit = EXCLUDED.outfit,
                location = EXCLUDED.location,
                updated_at = now()
        """
        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, row)
            return True
        except Exception as e:
            print(f"Failed to save hourly_plan: {e}")
            return False

    async def get_by_today_after_six(
        self,
    ) -> list[dict]:
        query = """
                SELECT
                    timeslot,
                    title,
                    description,
                    outfit,
                    location
                FROM hourly_plans
                WHERE created_at >= CURRENT_DATE + INTERVAL '5 hours'  
                AND created_at < CURRENT_TIMESTAMP;             
            """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                )

                rows = await cursor.fetchall()

        return [dict(row) for row in rows]
