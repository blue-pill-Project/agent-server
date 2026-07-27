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
            print(f"Failed to save visual prompt reference: {e}")
            return False

    async def search(
        self,
        category: str,
        query_vector: list[float],
    ):
        query = """
            SELECT
                id,
                category,
                participant_count,
                prompt,
                embedding <=> %s::vector AS distance
            FROM prompt_references
            WHERE category = %s
            ORDER BY embedding <=> %s::vector
            LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (query_vector, category, query_vector),
                )
                row = await cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row["id"],
            "category": row["category"],
            "participant_count": row["participant_count"],
            "prompt": row["prompt"],
        }
