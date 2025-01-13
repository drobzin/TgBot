from sqlalchemy.orm import Session
from sqlalchemy import event
from .database import async_session, engine, Base
from .models import Note, Subject

import logging


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Слушатель на удаление Note

@event.listens_for(Note, "after_delete")
def delete_subject_if_no_notes(mapper, connection, target):
    session = Session.object_session(target)
    logging.error('оно работает')
    if not session:
        return

    # Проверяем, остались ли связанные записи Note
    notes_count = session.query(Note).filter_by(
        subject_id=target.subject_id).count()
    if notes_count == 0:
        # Удаляем Subject, если больше нет Note
        session.query(Subject).filter_by(id=target.subject_id).delete()
