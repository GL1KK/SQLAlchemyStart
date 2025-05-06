from sqlalchemy import text, insert
from database import async_engine, sync_engine
from models import metadata_obj, workers_table


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
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine) # удаление
    print("Таблица удалена") 
    metadata_obj.create_all(sync_engine) # создание
    print("Таблица создана") 
    sync_engine.echo = True
# Запрос на вставку(INSERT)
def insert_data():
    with sync_engine.connect() as conn:
        # stmt = """INSERT INTO workers (username)  VALUES # ТАК НЕ НАДА
        # ('Bobr'),
        # ('Volk');"""
        stmt = insert(workers_table).values([ # Вот так нада
            {"username": "Bobr"},
            {"username": "Volk"}
        ])
        conn.execute(stmt)
        conn.commit() # после этого окажутся в бд