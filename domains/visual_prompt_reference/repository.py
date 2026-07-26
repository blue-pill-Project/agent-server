from psycopg_pool import AsyncConnectionPool


class VisualPromptReferenceRepository:
    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def save(
        self,
        visual_prompt_reference: tuple,
    ) -> bool:
        if not visual_prompt_reference:
            return True

        query = """
            INSERT INTO prompt_references (
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
                    await cursor.execute(
                        query,
                        visual_prompt_reference,
                    )

            return True
        except Exception as e:
            print(f"Failed to save visual prompt references: {e}")
            return False
