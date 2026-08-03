from datetime import date

from psycopg_pool import AsyncConnectionPool


class DailyPlanRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def get_today(
        self, log_room_id: str, log_room_member_id: str, date: date
    ) -> bool:
        # 구현해야함
        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    SELECT
                        daily_plan_id,
                        date,
                        day,
                        plan
                    FROM daily_plans
                    WHERE log_room_id = %s
                    AND log_room_member_id = %s
                    AND date = %s
                    """,
                    (log_room_id, log_room_member_id, date),
                )

                row = await cursor.fetchone()

        if row is None:
            return None

        return {
            "daily_plan_id": row["daily_plan_id"],
            "date": row["date"],
            "day": row["day"],
            "plan": row["plan"],
        }

    async def delete_by_room(self, log_room_id: str) -> None:
        """방 삭제 시 해당 방의 daily_plans 전체 삭제."""
        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "DELETE FROM daily_plans WHERE log_room_id = %s",
                    (log_room_id,),
                )

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
