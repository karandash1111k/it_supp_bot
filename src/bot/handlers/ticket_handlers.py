from vkbottle.bot import Message
from src.services.api.simleone import SimpleOneAPI
from src.core.states import UserStates
from src.utils.keyboards import (
    get_categories_keyboard,
    get_subcategories_keyboard,
    get_file_upload_keyboard,
    get_main_menu_keyboard,
    get_ticket_actions_keyboard
)
from src.core.config import Config

# инициализация API для работы с тикет-системой
simpleone_api = SimpleOneAPI()

# обработчик начала создания заявки
async def create_ticket_handler(message: Message):
    if not message.state.get("authenticated"):
        await message.answer("Сначала авторизуйтесь")
        return

    await message.answer(
        "Выберите категорию проблемы:",
        keyboard=get_categories_keyboard()
    )
    await message.state.set_state(UserStates.CATEGORY_SELECTION)

# обработчик выбора категории
async def category_selection_handler(message: Message):
    if message.text not in Config.CATEGORIES:
        await message.answer("Пожалуйста, выберите категорию из списка.")
        return

    message.state["category"] = message.text
    await message.answer(
        f"Вы выбрали категорию: {message.text}\nТеперь выберите подкатегорию:",
        keyboard=get_subcategories_keyboard(message.text)
    )
    await message.state.set_state(UserStates.SUBCATEGORY_SELECTION)

# обработчик выбора подкатегории
async def subcategory_selection_handler(message: Message):
    category = message.state.get("category")
    if message.text == "Назад":
        await message.answer(
            "Выберите категорию проблемы:",
            keyboard=get_categories_keyboard()
        )
        await message.state.set_state(UserStates.CATEGORY_SELECTION)
        return

    if message.text not in Config.CATEGORIES.get(category, []):
        await message.answer("Пожалуйста, выберите подкатегорию из списка.")
        return

    message.state["subcategory"] = message.text
    await message.answer(
        f"Вы выбрали подкатегорию: {message.text}\nТеперь подробно опишите проблему:"
    )
    await message.state.set_state(UserStates.PROBLEM_DESCRIPTION)

# обработчик описания проблемы
async def problem_description_handler(message: Message):
    message.state["description"] = message.text
    await message.answer(
        "Если нужно, прикрепите файлы (скриншоты, логи и т.д.).\n"
        "Или нажмите 'Нет файлов'.",
        keyboard=get_file_upload_keyboard()
    )
    await message.state.set_state(UserStates.FILE_UPLOAD)

# обработчик загрузки файлов и создания заявки
async def file_upload_handler(message: Message):
    email = message.state.get("email")
    if not email:
        await message.answer("Ошибка авторизации")
        return

    # вариант без файлов
    if message.text == "Нет файлов":
        attachments = []
    else:
        attachments = []
        if message.attachments:
            for attachment in message.attachments:
                if attachment.doc:
                    attachments.append(attachment.doc.url)
                elif attachment.photo:
                    sizes = attachment.photo.sizes
                    max_size = max(sizes, key=lambda s: s.width * s.height)
                    attachments.append(max_size.url)

    # создание заявки
    ticket = await simpleone_api.create_ticket(
        email=email,
        category=message.state["category"],
        subcategory=message.state["subcategory"],
        description=message.state["description"],
        attachments=attachments
    )

    if ticket:
        ticket_id = ticket.get("id", "N/A")
        await message.answer(
            f"✅ Заявка #{ticket_id} успешно создана!",
            keyboard=get_ticket_actions_keyboard()
        )
    else:
        await message.answer(
            "⚠️ Произошла ошибка при создании заявки.",
            keyboard=get_main_menu_keyboard()
        )
    await message.state.finish()

# обработчик просмотра существующих заявок
async def my_tickets_handler(message: Message):
    email = message.state.get("email")
    if not email:
        await message.answer("Сначала авторизуйтесь")
        return

    tickets = await simpleone_api.get_user_tickets(email)
    if tickets is None:
        await message.answer(
            "⚠️ Произошла ошибка при получении списка заявок.",
            keyboard=get_main_menu_keyboard()
        )
    elif not tickets:
        await message.answer(
            "У вас нет активных заявок.",
            keyboard=get_main_menu_keyboard()
        )
    else:
        response = "📋 Ваши заявки:\n\n"
        for ticket in tickets[:10]:
            response += (
                f"🔹 #{ticket.get('id', 'N/A')}\n"
                f"📌 Тема: {ticket.get('title', 'Без названия')}\n"
                f"🔄 Статус: {ticket.get('status', 'Неизвестен')}\n\n"
            )
        await message.answer(response, keyboard=get_main_menu_keyboard())

# обработчик дополнительной информации по заявке
async def additional_info_handler(message: Message):
    await message.answer("Введите дополнительную информацию по вашей заявке:")
    await message.state.set_state(UserStates.ADDITIONAL_INFO)

async def additional_info_text_handler(message: Message):
    message.state["additional_text"] = message.text
    await message.answer(
        "Если нужно, прикрепите файлы (скриншоты, логи и т.д.).\n"
        "Или нажмите 'Нет файлов'.",
        keyboard=get_file_upload_keyboard()
    )
    await message.state.set_state(UserStates.FILE_UPLOAD)