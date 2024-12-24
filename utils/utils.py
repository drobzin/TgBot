import asyncio
import re

from aiogram.types import Message

from keyboards.note_kb import rule_note_kb


def transform_string(input_string):
    # Разделяем строку по запятым
    words = input_string.split(',')
    # Убираем лишние пробелы, приводим к нижнему регистру и заменяем множественные пробелы на один
    cleaned_words = [re.sub(' +', ' ', word.strip().lower())
                     for word in words if word.strip()]
    # Объединяем слова обратно в строку через запятую
    result = ','.join(cleaned_words)
    return result


def get_content_info(message: Message):
    content_type = None
    file_id = None

    if message.document:
        content_type = "document"
        file_id = message.document.file_id

    content_text = message.text or message.caption
    return {'content_type': content_type, 'file_id': file_id, 'content_text': content_text}


async def send_message_user(bot, user_id, content_type, content_text=None, file_id=None, kb=None):

    if content_type == 'document':
        await bot.send_document(chat_id=user_id, document=file_id, caption=content_text, reply_markup=kb)


async def send_many_notes(all_notes, bot, user_id):
    for note in all_notes:
        try:
            await send_message_user(bot=bot, content_type=note['content_type'],
                                    content_text=note['content_text'],
                                    user_id=user_id,
                                    file_id=note['file_id'],
                                    kb=rule_note_kb(note['id']))
        except Exception as E:
            print(f'Error: {E}')
            await asyncio.sleep(2)
        finally:
            await asyncio.sleep(0.5)
