import os
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")


def create_db_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(
        conninfo=DATABASE_URL,
        min_size=2,
        max_size=10,
        timeout=10,
        open=False,
        kwargs={
            "row_factory": dict_row,
        },
    )
