from psycopg_pool import AsyncConnectionPool


class TrendRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def get_by_month(
        self,
        trend_month: str,
    ) -> list[dict]:
        query = """
            SELECT
                title,
                category,
                location,
                summary
            FROM trends
            WHERE trend_month = %s
            ORDER BY category, title
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (trend_month,),
                )

                rows = await cursor.fetchall()

        return [dict(row) for row in rows]

    async def save_all(
        self,
        trends: list,
    ) -> bool:
        if not trends:
            return True

        query = """
        INSERT INTO trends (
            trend_month, title, category, location, summary
        )
        VALUES (%s, %s, %s, %s, %s)
        """

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.executemany(query, trends)
            return True

        except Exception as e:
            print(f"Failed to save trends: {e}")
            return False
