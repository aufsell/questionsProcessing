from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def contact_keyboard():
    kb = [
        [KeyboardButton(
            text="Отправить номер телефона",
            request_contact=True)],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    return keyboard


async def approve_register():

    buttons = [
        [KeyboardButton(text=("Зарегистрироваться"))],
        [KeyboardButton(text=("Заново"))],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons)
    return keyboard
