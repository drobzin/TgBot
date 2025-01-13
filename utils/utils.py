import asyncio
import re

from aiogram.types import Message

from keyboards.note_kb import rule_note_kb
from data_base.dao import get_subject_name_by_id


def get_content_info(message: Message):
    content_type = None
    file_id = None

    if message.document:
        content_type = "document"
        file_id = message.document.file_id

    content_text = message.text or message.caption
    return {'content_type': content_type, 'file_id': file_id, 'content_text': content_text}


async def send_message_user(bot, user_id, content_type, content_text=None, subject_id=None, file_id=None, kb=None):
    subject_name = await get_subject_name_by_id(subject_id)
    if not content_text:
        content_text = ''
    if content_type == 'document':
        await bot.send_document(chat_id=user_id, document=file_id, caption=f'{content_text}\n\nПредмет - \'{subject_name}\' ', reply_markup=kb)


async def send_many_notes(all_notes, bot, user_id):
    for note in all_notes:
        try:
            await send_message_user(bot=bot, content_type=note['content_type'],
                                    content_text=note['content_text'],
                                    subject_id=note['subject_id'],
                                    user_id=user_id,
                                    file_id=note['file_id'],
                                    kb=rule_note_kb(note['id']))
        except Exception as E:
            print(f'Error: {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)
