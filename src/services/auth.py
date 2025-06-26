from src.models.user import User
from src.services.email import EmailService

# менеджер аутентификации пользователей
class AuthManager:

    # процесс аутентификации
    @staticmethod
    async def start_auth(email: str, vk_id: int) -> bool:
        if not email.endswith('@ranepa.ru'):
            return False

        # получение существующего пользователя или создание нового
        user = await User.get_by_email(email) or User(email, vk_id)
        await user.save()

        # отправление кода на email и возвращение результата
        code = await user.create_verification_code()
        return await EmailService.send_verification_code(
            email=email,
            code=code
        )

    # проверка кода верификации
    @staticmethod
    async def verify_code(email: str, code: str) -> bool:
        user = await User.get_by_email(email)
        if not user:
            return False
        return await user.verify(code)