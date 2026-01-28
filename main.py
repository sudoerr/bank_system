from db import DatabasePool, get_db, init_db, init_schema, UserRepo, UserStatus



async def main():
    init_db("connstr")
    pool = get_db()
    
    if not init_schema(pool=pool):
        return
    
    ...


