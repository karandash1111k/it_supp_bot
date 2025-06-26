from datetime import datetime, timedelta
import random
from typing import Optional
from src.services.database import Database

class User:
    # инициализация объекта пользователя системы
    def __init__(self, email: str, vk_id: Optional[int] = None, is_verified: bool = False):
        self.email = email
        self.vk_id = vk_id
        self.is_verified = is_verified

    # генерация кода подтверждения
    @staticmethod
    def generate_verification_code() -> str:
        return str(random.randint(100000, 999999))


    #        Получение пользователя из БД по email.

    #           Args:
    #                email (str): Email для поиска

    #        Returns:
    #                Optional[User]: Объект пользователя или None если не найден
    @classmethod
    async def get_by_email(cls, email: str) -> Optional['User']:
        record = await Database.fetchrow(
            "SELECT email, vk_id, is_verified FROM users WHERE email = $1",
            email
        )
        if record:
            return cls(**record)
        return None

    # сохранение пользователя в бд
    async def save(self):
        await Database.execute("""
            INSERT INTO users (email, vk_id, is_verified)
            VALUES ($1, $2, $3)
            ON CONFLICT (email) DO UPDATE
            SET vk_id = EXCLUDED.vk_id,
                is_verified = EXCLUDED.is_verified,
                updated_at = NOW()
        """,
            self.email, self.vk_id, self.is_verified)

    # создание и сохранение кода верификации
    async def create_verification_code(self) -> str:
        code = self.generate_verification_code()
        expires_at = datetime.now() + timedelta(minutes=10)

        await Database.execute("""
            INSERT INTO verification_codes (email, code, expires_at)
            VALUES ($1, $2, $3)
            ON CONFLICT (email) DO UPDATE
            SET code = EXCLUDED.code,
                expires_at = EXCLUDED.expires_at,
                created_at = NOW()
        """, self.email, code, expires_at)

        return code

    # проверка кода верификации
    async def verify(self, code: str) -> bool:
        record = await Database.fetchrow("""
            SELECT code, expires_at FROM verification_codes
            WHERE email = $1 AND expires_at > NOW()
            ORDER BY created_at DESC
            LIMIT 1
        """,
            self.email)

        if record and record['code'] == code:
            self.is_verified = True
            await self.save()
            await Database.execute(
                "DELETE FROM verification_codes WHERE email = $1",
                self.email
            )
            return True
        return False