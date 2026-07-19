from common.db.connection import get_connection


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
