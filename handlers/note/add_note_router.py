from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao import add_note, get_notes_by_user, get_subjects_by_user
from keyboards.note_kb import main_note_kb, add_note_check, generate_subject_keyboard
from keyboards.other_kb import stop_fsm
from utils.utils import get_content_info, send_message_user

add_note_router = Router()

subject_id = None


class AddNoteStates(StatesGroup):
    content = State()  # Ожидаем любое сообщение от пользователя
    choose_subject = State()  # Финальна проверка


@add_note_router.message(F.text == '📝 Отчеты')
async def start_note(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Можешь добавить отчет, выбери необходимое действие',
                         reply_markup=main_note_kb())


@add_note_router.message(F.text == '📝 Скинуть отчет')
async def start_add_note(message: Message, state: FSMContext):
    await state.clear()
    global subject_id
    subject_id = None
    all_subjects = await get_subjects_by_user(user_id=message.from_user.id)
    if all_subjects:
        await message.answer('По какому предмету отчет?', reply_markup=generate_subject_keyboard(all_subjects))

    else:
        await state.clear()
        await message.answer('У вас пока нет предметов для отчетов, их необходимо сначала добавить', reply_markup=main_note_kb())

    # await message.answer('Скидывай документ',reply_markup=stop_fsm())
    # await state.set_state(AddNoteStates.choose_subject)


@add_note_router.callback_query(F.data.startswith('subject_'))
async def add_subject_to_note(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    subject = call.data.replace('subject_', '')
    global subject_id
    subject_id = subject
    await call.message.answer('Отправтье файл')
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
            'Это что?'
        )
        await state.set_state(AddNoteStates.content)


""" @add_note_router.message(AddNoteStates.check_state, F.text == '✅ Все верно')
async def confirm_add_note(message: Message, state: FSMContext):
    note = await state.get_data()
    await add_note(user_id=message.from_user.id, content_type=note.get('content_type'),
                   content_text=note.get('content_text'), file_id=note.get('file_id'))
    await message.answer('Заметка успешно добавлена!', reply_markup=main_note_kb())
    await state.clear()


@add_note_router.message(AddNoteStates.check_state, F.text == '❌ Отменить')
async def cancel_add_note(message: Message, state: FSMContext):
    await message.answer('Добавление заметки отменено!', reply_markup=main_note_kb())
    await state.clear()
 """
