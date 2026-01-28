
from . import DatabasePool

from . import get_db


SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
    user_id BIGSERIAL PRIMARY KEY,
    phone VARCHAR(24) NOT NULL,
    role VARCHAR(12) NOT NULL DEFAULT 'user' CHECK(role IN ('founder', 'admin', 'user')),
    firstname VARCHAR(40),
    lastname VARCHAR(40),
    national_code VARCHAR(10),
    address TEXT,
    zip_code VARCHAR(24),
    status VARCHAR(12) NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'deactivated', 'limited', 'banned'))
);
"""

async def init_schema(pool: DatabasePool) -> bool:
    try:
        async with pool.get_conn() as conn:
            async with conn.cursor() as cur:
                await cur.execute(SCHEMA)
    except:
        # ToDo: implement logging for debug
        return False
    return True