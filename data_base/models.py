from sqlalchemy import BigInteger, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base


# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    # Связи с отчетами и напоминаниями
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="user", cascade="all, delete-orphan")
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="user", cascade="all, delete-orphan")


# Модель для таблицы отчетов
class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    subject_id: Mapped[int] = mapped_column(
        ForeignKey('subjects.id'), nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=True)
    content_text: Mapped[str] = mapped_column(Text, nullable=True)
    file_id: Mapped[str] = mapped_column(String, nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="notes")
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="notes")


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    full_name: Mapped[int] = mapped_column(String)
    user: Mapped["User"] = relationship("User", back_populates="subjects")
    notes: Mapped[list["Note"]] = relationship(
        "Note", back_populates="subject", cascade="all, delete-orphan")
