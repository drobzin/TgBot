from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao import get_notes_by_user, get_subjects_by_user, get_subject_by_id
from keyboards.note_kb import main_note_kb, find_note_kb, generate_subject_keyboard_withId
from utils.utils import send_many_notes


find_note_router = Router()


class FindNoteStates(StatesGroup):
    text = State()
    show_notes = State()  # Ожидаем текст для поиска отчета


@find_note_router.message(F.text == '📋 Просмотр отчетов')
async def start_views_noti(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Выбери какие отчеты отобразить', reply_markup=find_note_kb())


@find_note_router.message(F.text == '📄 Все отчеты')
async def all_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_notes_by_user(user_id=message.from_user.id)
    if all_notes:
        await send_many_notes(all_notes, bot, message.from_user.id)
        await message.answer(f'Все ваши {len(all_notes)} отчетов отправлены!', reply_markup=main_note_kb())
    else:
        await message.answer('У вас пока нет ни одного отчета!', reply_markup=main_note_kb())


@find_note_router.message(F.text == '🔍 По предмету')
async def subject_views_noti(message: Message, state: FSMContext):
    await state.clear()
    global subject_id
    subject_id = None
    all_subjects = await get_subjects_by_user(user_id=message.from_user.id)
    if all_subjects:
        await state.set_state(FindNoteStates.show_notes)
        await message.answer('По какому предмету отчет?', reply_markup=generate_subject_keyboard_withId(all_subjects))

    else:
        await state.clear()
        await message.answer('У вас пока нет предметов для отчетов, их необходимо сначала добавить', reply_markup=main_note_kb())


@find_note_router.callback_query(FindNoteStates.show_notes, F.data.startswith('subject_'))
async def find_note_to_subject(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    subject_id = int(call.data.replace('subject_', ''))
    all_notes = await get_notes_by_user(user_id=call.from_user.id, subject_id=subject_id)
    subject = await get_subject_by_id(subject_id)
    await call.message.answer_photo(photo=subject['file_id'], caption=f'Файлы по предмету \'{subject['full_name']}\'')
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши отчеты по предмету {subject['full_name']} отправлены!',
                              reply_markup=main_note_kb())
