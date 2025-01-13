from create_bot import logger
from .base import connection
from .models import User, Note, Subject
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError


@connection
async def set_user(session, tg_id: int, username: str, full_name: str) -> Optional[User]:
    try:
        user = await session.scalar(select(User).filter_by(id=tg_id))

        if not user:
            new_user = User(id=tg_id, username=username, full_name=full_name)
            session.add(new_user)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Пользователь с ID {tg_id} найден!")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection
async def add_note(session, user_id: int, subject_id: int, content_type: str,
                   content_text: Optional[str] = None, file_id: Optional[str] = None) -> Optional[Note]:
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None

        new_note = Note(
            user_id=user_id,
            subject_id=subject_id,
            content_type=content_type,
            content_text=content_text,
            file_id=file_id
        )

        session.add(new_note)
        await session.commit()
        logger.info(f"Отчет для пользователя с ID {
                    user_id} успешно добавлен!")
        return new_note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении отчета: {e}")
        await session.rollback()


@connection
async def add_subject(session, user_id: int, full_name: str) -> Optional[Subject]:
    try:
        user = await session.scalar(select(User).filter_by(id=user_id))
        if not user:
            logger.error(f"Пользователь с ID {user_id} не найден.")
            return None

        new_subject = Subject(
            user_id=user_id,
            full_name=full_name
        )

        session.add(new_subject)
        await session.commit()
        logger.info(f"Предмет для пользователя с ID {
                    user_id} успешно добавлен!")
        return new_subject
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении предмета: {e}")
        await session.rollback()


@connection
async def get_note_by_id(session, note_id: int) -> Optional[Dict[str, Any]]:
    try:
        note = await session.get(Note, note_id)
        if not note:
            logger.info(f"Отчет с ID {note_id} не найден.")
            return None

        return {
            'id': note.id,
            'content_type': note.content_type,
            'content_text': note.content_text,
            'file_id': note.file_id
        }
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении отчета: {e}")
        return None


@connection
async def delete_note_by_id(session, note_id: int) -> Optional[Note]:
    try:
        note = await session.get(Note, note_id)
        if not note:
            logger.error(f"Отчет с ID {note_id} не найден.")
            return None

        await session.delete(note)
        await session.commit()
        logger.info(f"Отчет с ID {note_id} успешно удален.")
        return note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении отчета: {e}")
        await session.rollback()
        return None


@connection
async def get_notes_by_user(session, user_id: int, date_add: str = None, text_search: str = None,
                            content_type: str = None, subject_id: int = None) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Note).filter_by(user_id=user_id))
        notes = result.scalars().all()
        if not notes:
            logger.info(f"Отчеты для пользователя с ID {user_id} не найдены.")
            return []

        note_list = [
            {
                'id': note.id,
                'content_type': note.content_type,
                'content_text': note.content_text,
                'file_id': note.file_id,
                'date_created': note.created_at,
                'subject_id': note.subject_id
            } for note in notes
        ]

        if date_add:
            note_list = [note for note in note_list if note['date_created'].strftime(
                '%Y-%m-%d') == date_add]

        if text_search:
            note_list = [note for note in note_list if text_search.lower() in (
                note['content_text'] or '').lower()]

        if content_type:
            note_list = [
                note for note in note_list if note['content_type'] == content_type]

        if subject_id:
            note_list = [
                note for note in note_list if note['subject_id'] == subject_id]

        return note_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении отчетов: {e}")
        return []


@connection
async def get_subjects_by_user(session, user_id: int) -> List[Dict[str, Any]]:
    try:
        result = await session.execute(select(Subject).filter_by(user_id=user_id))
        subjects = result.scalars().all()

        if not subjects:
            logger.info(f"Предметы для пользователя с ID {
                        user_id} не найдены.")
            return []

        subject_list = [
            {
                'id': subject.id,
                'full_name': subject.full_name
            } for subject in subjects
        ]
        return subject_list
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении отчетов: {e}")
        return []


@connection
async def get_subject_name_by_id(session, subject_id: int) -> List[Dict[str, Any]]:
    try:
        subject = await session.get(Subject, subject_id)
        if not subject:
            logger.info(f"Предмет с ID {subject_id} не найден.")
            return None

        return subject.full_name
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении предмета: {e}")
        return None


@connection
async def update_text_note(session, note_id: int, content_text: str) -> Optional[Note]:
    try:
        note = await session.scalar(select(Note).filter_by(id=note_id))
        if not note:
            logger.error(f"Отчет с ID {note_id} не найден.")
            return None

        note.content_text = content_text
        await session.commit()
        logger.info(f"Отчет с ID {note_id} успешно обновлен!")
        return note
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении отчета: {e}")
        await session.rollback()
