from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu(admin=False):
    base = [
        [KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="📧 Почта"), KeyboardButton(text="🌐 Домен")],
        [KeyboardButton(text="🔑 Доступы"), KeyboardButton(text="📚 Мануалы")]
    ]

    if admin:
        base.append([KeyboardButton(text="📊 Дашборд")])
        base.append([KeyboardButton(text="🛠 Админ")])

    return ReplyKeyboardMarkup(keyboard=base, resize_keyboard=True)