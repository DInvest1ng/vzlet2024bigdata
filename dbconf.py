from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import logging

# Создание базового класса для моделей
Base = declarative_base()

# Модель для пользователей
class User(Base):
    __tablename__ = 'users'
    telegram_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    username = Column(String)
    google_calendar_link = Column(String)

# Модель для чатов
class Chat(Base):
    __tablename__ = 'chats'
    telegram_chat_id = Column(Integer, unique=True, nullable=False, primary_key=True)
    chat_title = Column(String)

# Модель для связи пользователей и чатов
class UserChat(Base):
    __tablename__ = 'user_chats'
    telegram_id = Column(Integer, ForeignKey('users.telegram_id'), primary_key=True)
    telegram_chat_id = Column(Integer, ForeignKey('chats.telegram_chat_id'), primary_key=True)
    user = relationship("User")
    chat = relationship("Chat")

engine = create_engine('sqlite:///telegram_bot.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_user(telegram_id, username, google_calendar_link=None):
    user = User(telegram_id=telegram_id, username=username, google_calendar_link=google_calendar_link)
    session.add(user)
    session.commit()

def add_chat(telegram_chat_id, chat_title):
    chat = Chat(telegram_chat_id=telegram_chat_id, chat_title=chat_title)
    session.add(chat)
    session.commit()

def add_user_to_chat(telegram_id, telegram_chat_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).one()
    chat = session.query(Chat).filter_by(telegram_chat_id=telegram_chat_id).one()
    user_chat = UserChat(telegram_id=user.telegram_id, telegram_chat_id=chat.telegram_chat_id)
    session.add(user_chat)
    session.commit()

def remove_user_from_chat(telegram_id, telegram_chat_id):
    user = session.query(User).filter_by(telegram_id=telegram_id).one()
    chat = session.query(Chat).filter_by(telegram_chat_id=telegram_chat_id).one()
    user_chat = session.query(UserChat).filter_by(telegram_id=user.telegram_id, telegram_chat_id=chat.telegram_chat_id).one()
    session.delete(user_chat)
    session.commit()