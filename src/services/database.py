import asyncpg
from src.core.config import Config
from typing import Optional, Dict, Any

# класс для работы с базой данных PostgreSQL с использованием пула соединений
class Database:
    _pool: asyncpg.Pool = None

    # создание пула соединений с бд/возвращение существующего
    @classmethod
    async def get_pool(cls) -> asyncpg.Pool:
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                host=Config.DB_HOST,
                port=Config.DB_PORT
            )
        return cls._pool

    # запрос без возврата результата
    @classmethod
    async def execute(cls, query: str, *args) -> Optional[asyncpg.Record]:
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.execute(query, *args)

    # запрос со строкой результата
    @classmethod
    async def fetchrow(cls, query: str, *args) -> Optional[asyncpg.Record]:
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    # инициализация структуры. Вызывается при старте
    @classmethod
    async def init_db(cls):
        pool = await cls.get_pool()
        async with pool.acquire() as conn:
            await conn.execute("""
                --таблица пользователей--
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    vk_id INTEGER,
                    is_verified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                );
                --таблица верификации--
                CREATE TABLE IF NOT EXISTS verification_codes (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) NOT NULL,
                    code VARCHAR(6) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    FOREIGN KEY (email) REFERENCES users (email) ON DELETE CASCADE
                );
                --индекс для быстрого поиска по email--
                CREATE INDEX IF NOT EXISTS idx_verification_codes_email ON verification_codes (email);
            """)