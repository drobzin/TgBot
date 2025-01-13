from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from data_base.dao import add_note, get_subjects_by_user
from keyboards.note_kb import main_note_kb,  generate_subject_keyboard_withId
from keyboards.other_kb import stop_fsm
from utils.utils import get_content_info

add_note_router = Router()

subject_id = None


class AddNoteStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    choose_subject = State()  # Финальна проверка


@add_note_router.message(F.text == '🔙 Назад')
@add_note_router.message(F.text == '📝 Отчеты')
async def start_note(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выберите необходимое действие!',
                         reply_markup=main_note_kb())


@add_note_router.message(F.text == '📝 Отправить отчет')
async def start_add_note(message: Message, state: FSMContext):
    await state.clear()
    global subject_id
    subject_id = None
    all_subjects = await get_subjects_by_user(user_id=message.from_user.id)
    if all_subjects:
        await state.set_state(AddNoteStates.choose_subject)
        await message.answer('По какому предмету отчет? 🤔', reply_markup=generate_subject_keyboard_withId(all_subjects))

    else:
        await state.clear()
        await message.answer('У вас пока нет предметов для отчетов, их необходимо сначала добавить', reply_markup=main_note_kb())


@add_note_router.callback_query(AddNoteStates.choose_subject, F.data.startswith('subject_'))
async def add_subject_to_note(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    subject = call.data.replace('subject_', '')
    global subject_id
    subject_id = subject
    await call.message.answer('Отправтье файл', reply_markup=stop_fsm())
    await state.set_state(AddNoteStates.content)


@add_note_router.message(AddNoteStates.content)
async def handle_user_note_message(message: Message, state: FSMContext):
    content_info = get_content_info(message)
    if content_info.get('content_type'):
        global subject_id
        subject = subject_id
        await state.update_data(**content_info)

        note = await state.get_data()
        await add_note(user_id=message.from_user.id, subject_id=subject, content_type=note.get('content_type'),
                       content_text=note.get('content_text'), file_id=note.get('file_id'))
        await message.answer('Отчет добавлен', reply_markup=main_note_kb())

        await state.clear()
    else:
        await message.answer(
            'Прикрепите файл к сообщению'
        )
        await state.set_state(AddNoteStates.content)
