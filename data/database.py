from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from config import settings
import asyncio

# Создание движка(синхронный)

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_psyconf, # ссылка на БД
#     echo=False, # Типо логирование
#     pool_size=5, # Количество подключений
#     max_overflow=10, # Дополнительные подключения
# )

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, # ссылка на БД
    echo=False, # Типо логирование
    pool_size=5, # Количество подключений
    max_overflow=10, # Дополнительные подключения
)

# # Запрос (синхронный)
# with sync_engine.connect() as conn:
#     # получаем версию(без text не работает)
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res.first()=}")

# Запрос (асинхронный)
async def get():
    async with async_engine.connect() as conn:
        # получаем версию(без text не работает)
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}")

asyncio.run(get())

# #автокоммит
# with engine.begin() as conn:
#     # получаем версию(без text не работает)
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res}")
