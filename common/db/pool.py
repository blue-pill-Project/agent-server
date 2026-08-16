import os
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from common.config import settings


def create_db_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(
        conninfo=settings.DATABASE_URL,
        min_size=2,
        max_size=10,
        timeout=10,
        open=False,
        kwargs={
            "row_factory": dict_row,
            "autocommit": True,
        },
    )
