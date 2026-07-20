import os
from psycopg import connect


def save_daily_plans(
    plans: list,
) -> bool:
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return False

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
        with connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.executemany(query, plans)

            conn.commit()

        return True

    except Exception as e:
        print(f"Failed to save trends: {e}")
        return False
