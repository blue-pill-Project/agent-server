from datetime import date
import os
import psycopg
from psycopg.rows import dict_row
from common.db.connection import get_connection

def get_log_room_member_prompt(
    user_id: str, log_room_id: str, log_room_member_id: str
) -> dict:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return None

    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT cs.name, cs.description, cs.prompt
                FROM log_room_members lrm
                JOIN character_snapshots cs ON cs.snapshot_id = lrm.snapshot_id
                WHERE lrm.log_room_member_id = %s
                LIMIT 1
                """,
                (int(log_room_member_id),),
            )
            row = cur.fetchone()

    if not row:
        return None

    return {
        "name": row["name"],
        "description": row["description"],
        "prompt": row["prompt"],
    }
