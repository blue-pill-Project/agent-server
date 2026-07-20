from datetime import date
import os
import psycopg
from psycopg.rows import dict_row
from common.db.connection import get_connection


def get_trends(trend_month: date) -> list[dict]:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return []

    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    title,
                    category,
                    location,
                    summary
                FROM trends
                WHERE trend_month = %s
                ORDER BY category, title
                """,
                (trend_month,),
            )

            rows = cur.fetchall()

    return [dict(row) for row in rows]


def save_trends(
    trends: list,
    current_month: str,
) -> bool:

    if not trends.trends:
        return True

    query = """
    INSERT INTO trends (
        trend_month, title, category, location, summary
    )
    VALUES (%s, %s, %s, %s, %s)
    """

    rows = [
        (current_month, t.title, t.category, t.location, t.summary)
        for t in trends.trends
    ]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(query, rows)
        return True

    except Exception as e:
        print(f"Failed to save trends: {e}")
        return False
