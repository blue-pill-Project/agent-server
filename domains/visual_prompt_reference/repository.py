from typing import Any
from psycopg_pool import AsyncConnectionPool
from agents.visual_prompt_reference.state import VisualPromptReferenceForSave

#TODO: 예외를 처리해야함 지금 반환값 예외 처리 다 제각각임
class VisualPromptReferenceRepository:
    """
    Visual Prompt Reference의 저장 및 조회를 담당한다.

    PostgreSQL의 visual_prompt_references 테이블을 대상으로
    레퍼런스 저장, 벡터 유사도 검색, 기본 셀피 조회를 수행한다.

    methods
    - save: 레퍼런스 저장
    - search: 벡터 유사도 검색
    - get_random_default_selfie: 기본 셀피 랜덤 조회
    """

    def __init__(
        self,
        pool: AsyncConnectionPool,
    ):
        self._pool = pool

    async def save(
        self,
        visual_prompt_reference: VisualPromptReferenceForSave,
    ) -> bool:
        """
        Visual Prompt Reference를 데이터베이스에 저장한다.

        Args:
            visual_prompt_reference:
                visual_prompt_references 테이블에 저장할 값.

        Returns:
            저장에 성공하면 True, 실패하면 False.
        """

        query = """
            INSERT INTO visual_prompt_references (
                category,
                camera_style,
                participant_count,
                image_url,
                situation,
                situation_embedding,
                is_default_selfie
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        params = (
            visual_prompt_reference.category,
            visual_prompt_reference.camera_style,
            visual_prompt_reference.participant_count,
            visual_prompt_reference.image_key,
            visual_prompt_reference.situation,
            visual_prompt_reference.situation_embedding,
            visual_prompt_reference.is_default_selfie,
        )

        try:
            async with self._pool.connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, params)

            return True

        except Exception as e:
            print(f"Failed to save visual prompt reference: {e}")
            return False

    async def search(self, category: str, query_vector: list[float], limit: int)-> list[dict[str, Any]]:
        """
        카테고리와 벡터 유사도를 기준으로 레퍼런스를 검색한다.

        Args:
            category:
                검색할 이미지 카테고리.

            query_vector:
                현재 장면을 임베딩한 검색 벡터.

            limit:
                반환할 최대 검색 결과 개수.

        Returns:
            유사도가 높은 순서로 정렬된 레퍼런스 목록.
        """
        query = """
            SELECT
                  visual_prompt_reference_id,
                  category,
                  camera_style,
                  participant_count,
                  image_url,
                  situation,
                  1 - (situation_embedding <=> CAST(%s AS vector)) AS similarity
            FROM visual_prompt_references
            WHERE category = %s
            ORDER BY situation_embedding <=> CAST(%s AS vector)::vector
            LIMIT %s
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query,
                    (query_vector, category, query_vector, limit),
                )
                rows = await cursor.fetchall()

        return [dict(row) for row in rows]

    async def get_random_default_selfie(self)-> dict[str, Any] | None:
        """
        기본 셀피 레퍼런스 중 하나를 무작위로 조회한다.

        Returns:
            조회된 기본 셀피 레퍼런스.
            존재하지 않으면 None.
        """
        query = """
            SELECT
                visual_prompt_reference_id,
                category,
                camera_style,
                participant_count,
                image_url,
                situation
            FROM visual_prompt_references
            WHERE is_default_selfie = TRUE
            AND camera_style = 'selfie'
            ORDER BY RANDOM()
            LIMIT 1
        """

        async with self._pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query)
                row = await cursor.fetchone()

        if row is None:
            return None

        return row
