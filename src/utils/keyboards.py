from vkbottle import Keyboard, KeyboardButtonColor, Text
from src.core.config import Config

# клавиатура для главного меню
def get_main_menu_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(Text("Создать заявку"), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text("Мои заявки"), color=KeyboardButtonColor.PRIMARY)

    keyboard.row()
    keyboard.add(Text("Помощь"), color=KeyboardButtonColor.SECONDARY)

    return keyboard.get_json()

# клавиатура для выбора категории проблемы
def get_categories_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)

    for category in Config.CATEGORIES.keys():
        keyboard.add(Text(category), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()

    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)

    return keyboard.get_json()

# клавиатура для выбора подкатегории проблемы
def get_subcategories_keyboard(category):
    keyboard = Keyboard(one_time=True, inline=False)

    for subcategory in Config.CATEGORIES[category]:
        keyboard.add(Text(subcategory), color=KeyboardButtonColor.PRIMARY)
        keyboard.row()

    keyboard.add(Text("Назад"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)

    return keyboard.get_json()

# клавиатура для загрузки файлов
def get_file_upload_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)

    keyboard.add(Text("Нет файлов"), color=KeyboardButtonColor.SECONDARY)
    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)

    return keyboard.get_json()

# клавиатура действий с тикетом
def get_ticket_actions_keyboard():
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(Text("Дополнить заявку"), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Мои заявки"), color=KeyboardButtonColor.PRIMARY)

    keyboard.row()
    keyboard.add(Text("Главное меню"), color=KeyboardButtonColor.SECONDARY)

    return keyboard.get_json()
