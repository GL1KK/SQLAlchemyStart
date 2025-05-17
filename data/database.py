from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from config import settings
import asyncio
from typing import Annotated

# Создание синхронного движка SQLAlchemy
sync_engine = create_engine(
    url=settings.DATABASE_URL_psyconf, # Указываем URL для подключения к синхронной базе данных (например, PostgreSQL, SQLite).
    echo=True, # Если True, SQLAlchemy будет выводить в консоль все сгенерированные SQL-запросы (полезно для отладки).
    pool_size=5, # Устанавливаем начальный размер пула соединений (количество одновременно активных подключений к БД).
    max_overflow=10, # Определяем максимальное количество дополнительных соединений, которые могут быть созданы при перегрузке пула.
)

# Создание асинхронного движка SQLAlchemy (для асинхронной работы с базой данных)
async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, # Указываем URL для подключения к асинхронной базе данных (например, PostgreSQL с asyncpg).
    echo=False, # Отключаем вывод SQL-запросов для асинхронного движка.
    pool_size=5, # Устанавливаем начальный размер пула асинхронных соединений.
    max_overflow=10, # Определяем максимальное количество дополнительных асинхронных соединений.
)

# Создание фабрики сессий для синхронной работы с базой данных
sync_session_factory = sessionmaker(sync_engine) # 'sessionmaker' создает фабрику, которая при вызове генерирует объекты сессий,
                                               # использующие указанный синхронный движок. Сессия управляет всеми операциями
                                               # с базой данных для определенного "рабочего процесса".

# Создание фабрики сессий для асинхронной работы с базой данных
async_session_factory = async_sessionmaker(async_engine) # Аналогично 'sessionmaker', но для асинхронного движка.
                                                     # Асинхронные сессии используются с ключевыми словами 'async with'.

# Ограничение на длину строкового поля (использование typing.Annotated)
str_256 = Annotated[str, 256] # 'Annotated' используется для добавления метаданных к типам.
                               # В данном случае, мы создаем аннотированный тип 'str_256', указывая,
                               # что это строка с максимальной длиной 256 символов.
                               # SQLAlchemy будет использовать эту информацию при создании схемы базы данных.

# Базовый класс для определения ORM моделей (наследуются от него ваши таблицы)
class Base(DeclarativeBase):
    """
    Базовый класс для декларативного определения ORM моделей SQLAlchemy.
    Все ваши классы таблиц (например, WorkerOrm, ResumesOrm) должны наследоваться от этого класса.
    Он предоставляет механизм для определения таблиц как классов Python.
    """
    type_annotation_map = {
        str_256: String(256) # Указываем SQLAlchemy, что когда встречается аннотация типа 'str_256',
                             # соответствующий столбец в базе данных должен быть типа String с длиной 256.
    }