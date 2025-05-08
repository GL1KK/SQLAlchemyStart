from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, create_engine, text, String
from config import settings
import asyncio
from typing import Annotated

# Создание движка(синхронный)

sync_engine = create_engine(
    url=settings.DATABASE_URL_psyconf, # ссылка на БД
    echo=True, # Типо логирование
    pool_size=5, # Количество подключений
    max_overflow=10, # Дополнительные подключения
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, # ссылка на БД
    echo=False, # Типо логирование
    pool_size=5, # Количество подключений
    max_overflow=10, # Дополнительные подключения
)

# Сессии для удобсва как я понял типо циклы но для SQL
sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

# ограгичение
str_256 = Annotated[str, 256]

# Базовый класс для хранения данных
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }