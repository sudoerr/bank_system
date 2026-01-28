from enum import StrEnum
from psycopg.rows import dict_row

from . import DatabasePool


class UserStatus(StrEnum):
    active = "active"
    inactive = "deactivated"
    limited = "limited"
    banned = "banned"


class UserRepo:
    def __init__(self, pool: DatabasePool):
        self.__pool = pool

    async def add_user(
        self,
        phone: str,
        role: str,
        firstname: str,
        lastname: str,
        national_code: str,
        address: str,
        zip_code: str,
    ) -> bool:
        try:
            async with self.__pool.get_conn() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        INSERT INTO users(phone, role, firstname, lastname, national_code, address, zip_code)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            phone,
                            role,
                            firstname,
                            lastname,
                            national_code,
                            address,
                            zip_code,
                        ),
                    )
        except:
            # ToDo: implement logging for debug
            return False

        return True

    async def update_user(
        self,
        user_id: int,
        phone: str | None = None,
        role: str | None = None,
        firstname: str | None = None,
        lastname: str | None = None,
        national_code: str | None = None,
        address: str | None = None,
        zip_code: str | None = None,
    ) -> bool:
        try:
            async with self.__pool.get_conn() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        UPDATE users
                        set phone = COALESCE(%s, phone),
                            role = COALESCE(%s, role),
                            firstname = COALESCE(%s, firstname),
                            lastname= COALESCE(%s, lastname),
                            national_code = COALESCE(%s, national_code),
                            address = COALESCE(%s, address),
                            zip_code = COALESCE(%s, zip_code)
                        WHERE user_id = %s
                        """,
                        (
                            phone,
                            role,
                            firstname,
                            lastname,
                            national_code,
                            address,
                            zip_code,
                            user_id,
                        ),
                    )
        except:
            # ToDo: implement logging for debug
            return False

        return True

    async def set_user_status(self, user_id: int, level: UserStatus) -> bool:
        try:
            async with self.__pool.get_conn() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        UPDATE users
                        set status = %s
                        WHERE user_id = %s
                        """,
                        (level, user_id),
                    )
        except:
            # ToDo: implement logging for debug
            return False

        return True

    async def get_user(self, user_id: int | None = None, phone: str | None = None) -> dict|bool:
        if phone == user_id == None:
            raise RuntimeError("At least one of user_id or phone must be valid")
        try:
            async with self.__pool.get_conn() as conn:
                async with conn.cursor(row_factory=dict_row) as cur:
                    await cur.execute("SELECT * from users WHERE user_id=%s OR phone=%s", (user_id, phone))
                    return await cur.fetchone()
        except:
            # ToDo: implement logging for debug
            return False

    async def get_users(self, page: int = 1) -> list[dict]:
        pass # No need for now
