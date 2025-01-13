from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_date_keyboard(notes):
    unique_dates = {note['date_created'].strftime(
        '%Y-%m-%d') for note in notes}
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for date_create in unique_dates:
        button = InlineKeyboardButton(
            text=date_create, callback_data=f"date_note_{date_create}")
        keyboard.inline_keyboard.append([button])

    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="Главное меню", callback_data="main_menu")])

    return keyboard


def generate_subject_keyboard_withName(subjects):
    # unique_subjects = {subject['full_name'] for subject in subjects}

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for subject in subjects:
        button = InlineKeyboardButton(
            text=str(subject['full_name']), callback_data=f'subject_{subject['full_name']}')
        keyboard.inline_keyboard.append([button])

    return keyboard


def generate_subject_keyboard_withId(subjects):
    # unique_subjects = {subject['full_name'] for subject in subjects}

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for subject in subjects:
        button = InlineKeyboardButton(
            text=str(subject['full_name']), callback_data=f'subject_{subject['id']}')
        keyboard.inline_keyboard.append([button])

    return keyboard


def generate_type_content_keyboard(notes):
    unique_content = {note['content_type'] for note in notes}
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for content_type in unique_content:
        button = InlineKeyboardButton(
            text=content_type, callback_data=f"content_type_note_{content_type}")
        keyboard.inline_keyboard.append([button])

    keyboard.inline_keyboard.append([InlineKeyboardButton(
        text="Главное меню", callback_data="main_menu")])

    return keyboard


def main_note_kb():
    kb_list = [
        [KeyboardButton(text="📝 Отправить отчет"),
         KeyboardButton(text="📋 Просмотр отчетов"),
         KeyboardButton(text="🎓 Добавить предмет")],
        [KeyboardButton(text="🏠 Главное меню")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )


def find_note_kb():
    kb_list = [
        [KeyboardButton(text="📄 Все отчеты"),
         KeyboardButton(text="🔍 По предмету"), ],
        [KeyboardButton(text="🏠 Главное меню")]]

    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите опцию👇"
    )


def rule_note_kb(note_id: int,):
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Изменить текст", callback_data=f"edit_note_text_{note_id}")],
                         [InlineKeyboardButton(text="Удалить", callback_data=f"dell_note_{note_id}")]])


def add_note_check():
    kb_list = [
        [KeyboardButton(text="✅ Все верно"), KeyboardButton(text="❌ Отменить")]
    ]
    return ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйся меню👇"
    )
