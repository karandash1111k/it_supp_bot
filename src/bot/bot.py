from vkbottle import Bot, API
from vkbottle.bot import Message, rules
from src.bot.handlers import (
    start_handler,
    create_ticket_handler,
    my_tickets_handler,
    additional_info_handler,
    help_handler,
    cancel_handler,
    logout_handler,
    email_input_handler,
    code_verification_handler,
    category_selection_handler,
    subcategory_selection_handler,
    problem_description_handler,
    file_upload_handler,
    additional_info_text_handler
)
from src.core.states import UserStates
from src.core.middleware import UserDataMiddleware
from src.core.config import Config
from src.utils.keyboards import get_main_menu_keyboard
import logging
import warnings

warnings.filterwarnings("ignore", message="coroutine 'wait' was never awaited")

logger = logging.getLogger(__name__)

async def init_bot():
    try:
        # инициализация бота
        api = API(token=Config.VK_TOKEN)  # Явное создание API
        bot = Bot(api=api)
        bot.labeler.message_view.register_middleware(UserDataMiddleware)

        # правила для обработчиков
        message_rules = [rules.PeerRule(from_chat=False)]

        # регистрация обработчиков
        bot.on.private_message(*message_rules, text=["Начать", "Главное меню"])(start_handler)
        bot.on.private_message(*message_rules, text="Создать заявку")(create_ticket_handler)
        bot.on.private_message(*message_rules, text="Мои заявки")(my_tickets_handler)
        bot.on.private_message(*message_rules, text="Дополнить заявку")(additional_info_handler)
        bot.on.private_message(*message_rules, text="Помощь")(help_handler)
        bot.on.private_message(*message_rules, text="Отмена")(cancel_handler)
        bot.on.private_message(*message_rules, text="Выйти")(logout_handler)

        # обработчики состояний
        bot.on.private_message(state=UserStates.EMAIL_INPUT)(email_input_handler)
        bot.on.private_message(state=UserStates.CODE_VERIFICATION)(code_verification_handler)
        bot.on.private_message(state=UserStates.CATEGORY_SELECTION)(category_selection_handler)
        bot.on.private_message(state=UserStates.SUBCATEGORY_SELECTION)(subcategory_selection_handler)
        bot.on.private_message(state=UserStates.PROBLEM_DESCRIPTION)(problem_description_handler)
        bot.on.private_message(state=UserStates.FILE_UPLOAD)(file_upload_handler)
        bot.on.private_message(state=UserStates.ADDITIONAL_INFO)(additional_info_text_handler)

        # обработчик по умолчанию
        @bot.on.private_message()
        async def default_handler(message: Message):
            await message.answer(
                "Я не понял вашего сообщения. Пожалуйста, используйте кнопки меню.",
                keyboard=get_main_menu_keyboard()
            )

        logger.info("Обработчики успешно зарегистрированы")
        logger.info("Бот запущен")
        return bot

    except Exception as e:
        logger.error(f"Ошибка инициализации бота: {e}")
        raise
