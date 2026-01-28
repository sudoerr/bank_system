import psycopg
from psycopg_pool import AsyncConnectionPool
from contextlib import asynccontextmanager


class DatabasePool:
    def __init__(self, connstr: str):
        self.pool = AsyncConnectionPool(connstr, open=False)

    async def open(self):
        await self.pool.open()

    async def close(self):
        await self.pool.close()

    @asynccontextmanager
    async def get_conn(self):
        async with self.pool.connection() as conn:
            yield conn
