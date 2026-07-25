from psycopg_pool import AsyncConnectionPool


class VisualPromptReferenceRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def save_all(
        self,
        visual_prompt_references: tuple,
    ) -> bool:
        if not visual_prompt_references:
            return True

        query = """
            INSERT INTO visual_prompt_references (
                category,
                participant_count,
                prompt,
                embedding
            )
            VALUES (%s, %s, %s, %s)
        """

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.executemany(
                        query,
                        visual_prompt_references,
                    )

            return True
        except Exception as e:
            print(f"Failed to save visual prompt references: {e}")
            return False
