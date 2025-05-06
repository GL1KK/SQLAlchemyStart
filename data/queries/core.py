from sqlalchemy import text
from database import async_engine, sync_engine
from models import metadata_obj


# Запрос (синхронный)
def get_sync_vers():
    with sync_engine.connect() as conn:
        # получаем версию(без text не работает)
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}")

#автокоммит
# with sync_engine.begin() as conn:
#     # получаем версию(без text не работает)
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res}")

# Запрос (асинхронный)
async def get_async_123():
    async with async_engine.connect() as conn:
        # получаем (1, 2, 3)(4, 5, 6)(без text не работает)
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}")

# Создание таблицы
def create_table():
    metadata_obj.drop_all(sync_engine) # удаление
    metadata_obj.create_all(sync_engine) # создание
