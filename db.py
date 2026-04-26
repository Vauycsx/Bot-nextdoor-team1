import asyncpg
from config import DATABASE_URL

pool: asyncpg.Pool = None


async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            role TEXT
        )
        """)

        await conn.execute("CREATE TABLE IF NOT EXISTS codes (code TEXT)")
        await conn.execute("CREATE TABLE IF NOT EXISTS emails (value TEXT)")
        await conn.execute("CREATE TABLE IF NOT EXISTS domains (value TEXT)")
        await conn.execute("CREATE TABLE IF NOT EXISTS accesses (value TEXT)")
        await conn.execute("CREATE TABLE IF NOT EXISTS manuals (value TEXT)")