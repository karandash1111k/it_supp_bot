from vkbottle.bot import Message
from vkbottle import Keyboard, Text
from src.services.auth import AuthManager
from src.models.user import User
from src.core.states import UserStates
from src.utils.keyboards import get_main_menu_keyboard
import logging

logger = logging.getLogger(__name__)

# обработчик команды старта
async def start_handler(message: Message):
    try:
        await message.answer(
            "Добро пожаловать! Используйте кнопки меню:",
            keyboard=get_main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка в start_handler: {e}")

    # получение пользователя по email из состояния
    user = await User.get_by_email(message.state.get("email"))
    if user and user.is_verified:
        await get_main_menu_keyboard(message)
    else:
        await message.answer(
            "Для работы с ботом необходимо авторизоваться.\n"
            "Введите вашу корпоративную почту (@ranepa.ru):"
        )
        await message.state.set_state(UserStates.EMAIL_INPUT)

# обработчик ввода email
async def email_input_handler(message: Message):
    email = message.text.strip().lower()
    if not email.endswith('@ranepa.ru'):
        await message.answer("Пожалуйста, используйте корпоративную почту @ranepa.ru")
        return

    # процесс авторизации
    success = await AuthManager.start_auth(email, message.from_id)
    if success:
        message.state["email"] = email
        await message.answer(
            f"На почту {email} отправлен код подтверждения. "
            "Введите его здесь:"
        )
        await message.state.set_state(UserStates.CODE_VERIFICATION)
    else:
        await message.answer(
            "Не удалось отправить код подтверждения. Попробуйте позже."
        )

# обработчик ввода кода подтверждения
async def code_verification_handler(message: Message):
    email = message.state.get("email")
    if not email:
        await message.answer("Сначала введите email")
        return

    # получение и проверка кода
    code = message.text.strip()
    if await AuthManager.verify_code(email, code):
        await message.answer(
            "Авторизация прошла успешно!",
            keyboard=get_main_menu_keyboard()
        )
        await message.state.update({"authenticated": True})
    else:
        await message.answer(
            "Неверный код подтверждения или срок его действия истек. "
            "Попробуйте снова или запросите новый код."
        )

# обработчик выхода из системы
async def logout_handler(message: Message):
    await message.state.delete()
    await message.answer(
        "Вы вышли из системы. Для продолжения работы авторизуйтесь снова.",
        keyboard=Keyboard().add(Text("Начать")).get_json()
    )