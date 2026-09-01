from psycopg_pool import AsyncConnectionPool


class CharacterRepository:
    def __init__(self, pool: AsyncConnectionPool):
        self._pool = pool

    async def get_prompt(
        self,
        character_id: int,
    ) -> str | None:
        query = """
            SELECT prompt
            FROM character_cards
            WHERE character_id = %s
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (character_id,))
                row = await cursor.fetchone()

        return row["prompt"] if row else None

    async def get_example_dialogues(
        self,
        character_id: int,
    ) -> list[str]:
        query = """
            SELECT content
            FROM example_dialogues
            WHERE character_id = %s
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, (character_id,))
                rows = await cursor.fetchall()

        return [row["content"] for row in rows]
