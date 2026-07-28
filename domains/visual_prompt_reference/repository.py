from psycopg_pool import AsyncConnectionPool

from agents.subgraphs.generate_log_image.state import ImageCategory


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
            INSERT INTO visual_prompt_references (
                category,
                participant_count,
                prompt,
                situation,
                situation_embedding
            )
            VALUES (%s, %s, %s,%s, %s)
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
                  situation,
                  1 - (situation_embedding <=> CAST(%s AS vector)) AS similarity
            FROM visual_prompt_references
            WHERE category = %s
            ORDER BY situation_embedding <=> CAST(%s AS vector)::vector
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
            "situation": row["situation"],
        }
