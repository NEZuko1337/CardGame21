from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

choose_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Еще"),
            KeyboardButton(text="Хватит"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True,
)

start_new_game = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/startgame"),
            
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите действие из меню",
    selective=True,
)

default_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/startgame"),
            KeyboardButton(text="/help")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери действие из меню",
    selective=True
)

rmk = ReplyKeyboardRemove()