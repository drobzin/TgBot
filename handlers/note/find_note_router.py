from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from create_bot import bot
from data_base.dao import get_notes_by_user, get_subjects_by_user, get_subject_name_by_id
from keyboards.note_kb import main_note_kb, find_note_kb, generate_date_keyboard, generate_type_content_keyboard, generate_subject_keyboard_withId, generate_subject_keyboard_withName
from utils.utils import send_many_notes
from create_bot import logger


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
async def find_note_to_date(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    subject_id = int(call.data.replace('subject_', ''))
    all_notes = await get_notes_by_user(user_id=call.from_user.id, subject_id=subject_id)
    subject_name = await get_subject_name_by_id(subject_id)
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши отчеты по предмету {subject_name} отправлены!',
                              reply_markup=main_note_kb())

# TODO: УДАЛИТЬ


@find_note_router.message(F.text == '📝 По типу контента')
async def content_type_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_notes_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('Какой тип заметок по контенту вас интересует?',
                             reply_markup=generate_type_content_keyboard(all_notes))
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb())


@find_note_router.callback_query(F.data.startswith('content_type_note_'))
async def find_note_to_content_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    content_type = call.data.replace('content_type_note_', '')
    all_notes = await get_notes_by_user(user_id=call.from_user.id, content_type=content_type)
    await send_many_notes(all_notes, bot, call.from_user.id)
    await call.message.answer(f'Все ваши {len(all_notes)} с типом контента {content_type} отправлены!',
                              reply_markup=main_note_kb())

# TODO: удалить
""" @find_note_router.message(F.text == '🔍 Поиск по тексту')
async def text_views_noti(message: Message, state: FSMContext):
    await state.clear()
    all_notes = await get_notes_by_user(user_id=message.from_user.id)
    if all_notes:
        await message.answer('Введите поисковой запрос. После этого я начну поиск по заметкам. Если в текстовом '
                             'содержимом заметки будет обнаружен поисковой запрос, то я отображу эти заметки')
        await state.set_state(FindNoteStates.text)
    else:
        await message.answer('У вас пока нет ни одной заметки!', reply_markup=main_note_kb()) """

# TODO удалить


@find_note_router.message(F.text, FindNoteStates.text)
async def text_noti_process(message: Message, state: FSMContext):
    text_search = message.text.strip()
    all_notes = await get_notes_by_user(user_id=message.from_user.id, text_search=text_search)
    await state.clear()
    if all_notes:
        await send_many_notes(all_notes, bot, message.from_user.id)
        await message.answer(f'C поисковой фразой {text_search} было обнаружено {len(all_notes)} заметок!',
                             reply_markup=main_note_kb())
    else:
        await message.answer(f'У вас пока нет ни одной заметки, которая содержала бы в тексте {text_search}!',
                             reply_markup=main_note_kb())
