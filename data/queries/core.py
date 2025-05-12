from sqlalchemy import text, insert, select, update
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
def create_table_core():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine) # удаление
    print("Таблица удалена") 
    metadata_obj.create_all(sync_engine) # создание
    print("Таблица создана") 
    sync_engine.echo = True
# Запрос на вставку(INSERT)
def insert_data_core():
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
def select_workers_core():
    with sync_engine.connect() as conn:
        query = select(workers_table) # SELECT * FROM workers;
        res = conn.execute(query)
        workers = res.all()
        print(workers)
def update_workers_core(worker_id: int = 2, new_username: str = "Misha"):
    with sync_engine.connect() as conn:
        # stmt = text("UPDATE workers SET username={new_username}") # SQL иньекция так нельза!!!!
        # stmt = text("UPDATE workers SET username=:username WHERE id=:id") # Правильно(сырой запрос)
        # stmt = stmt.bindparams(username=new_username, id=workers_id) 
        stmt = update(workers_table).values(username=new_username).filter_by(id=worker_id) # where/filter(workers_table.c.id==workers_id) не оч
        conn.execute(stmt)
        conn.commit()