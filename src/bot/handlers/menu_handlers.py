from vkbottle.bot import Message
from src.utils.keyboards import get_main_menu_keyboard

# обработчик команды помощи
async def help_handler(message: Message):
    await message.answer(
        "🤖 IT Support Bot - помощь\n\n"
        "Этот бот предназначен для обращения в IT-поддержку.\n\n"
        "📌 Доступные команды:\n"
        "- Создать заявку: начать процесс создания новой заявки\n"
        "- Мои заявки: просмотреть список ваших заявок и их статус\n"
        "- Дополнить заявку: добавить информацию к существующей заявке\n\n"
        "Для начала работы нажмите 'Создать заявку' или выберите другое действие.",
        keyboard=get_main_menu_keyboard()
    )

# обработчик команды отмены
async def cancel_handler(message: Message):
    await message.answer(
        "Действие отменено. Выберите действие:",
        keyboard=get_main_menu_keyboard()
    )
    await message.state.finish() # сброс состояния диалога