from sqlalchemy import text, insert
from database import sync_engine, async_engine, sync_session_factory, async_session_factory, Base
from models import metadata_obj, WorkerOrm

def create_table():
    Base.metadata.drop_all(sync_engine) # удаление
    sync_engine.echo = True
    Base.metadata.create_all(sync_engine) # создание
    sync_engine.echo = True

# Запрос на вставку(INSERT)(синхронная сессия)
def insert_table():
    with sync_session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        # session.add(worker_bobr) # Отправка в сессию
        # session.add(worker_volk) или...
        session.add_all([worker_bobr, worker_volk])
        session.commit() # Тогда окажутся в БД

# Запрос на вставку(INSERT)(асинхронная сессия)
async def insert_table():
    async with async_session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        # session.add(worker_bobr) # Отправка в сессию
        # session.add(worker_volk) или...
        session.add_all([worker_bobr, worker_volk])
        await session.commit() # Тогда окажутся в БД