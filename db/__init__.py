from .conn import DatabasePool
from .users import UserRepo, UserStatus
from .schema import init_schema

_pool: DatabasePool | None = None


def init_db(connstr: str) -> DatabasePool:
    global _pool
    if _pool is None:
        _pool = DatabasePool(connstr)
    return _pool


def get_db() -> DatabasePool:
    if _pool is None:
        raise RuntimeError("DatabasePool is not initialized.")
    return _pool
