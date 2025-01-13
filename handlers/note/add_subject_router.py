from decouple import config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from create_bot import bot
from data_base.dao import add_note, add_subject, get_notes_by_user, get_subjects_by_user
from keyboards.note_kb import main_note_kb, add_note_check, generate_subject_keyboard_withId
from keyboards.other_kb import stop_fsm
from neural_networks.kandisky import Text2ImageAPI
from utils.utils import get_content_info


add_subject_router = Router()


class AddSubjectStates(StatesGroup):
    content = State()


@add_subject_router.message(F.text == '🎓 Добавить предмет')
async def add_subject_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Введи название предмета', reply_markup=stop_fsm())
    await state.set_state(AddSubjectStates.content)


# TODO: Раскоментить строчку
@add_subject_router.message(AddSubjectStates.content)
async def handle_user_subject_message(message: Message, state: FSMContext):
    await message.answer(text='Ожидайте! Делаю красоту 🎉')
    Text2ImageAPI.start_generate(message.text)
    msg = await message.answer_photo(photo=FSInputFile('images\image.jpg'), caption=f'Предмет - {message.text} успешно добавлен!', reply_markup=main_note_kb())
    photo_id = msg.photo[-1].file_id
    await add_subject(user_id=message.from_user.id, full_name=message.text, file_id=photo_id)
    await state.clear()
