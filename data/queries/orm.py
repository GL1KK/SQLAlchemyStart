from sqlalchemy import text, insert, select
from database import sync_engine, async_engine, sync_session_factory, async_session_factory, Base
from models import metadata_obj, WorkerOrm

def create_table_orm():
    Base.metadata.drop_all(sync_engine) # удаление
    sync_engine.echo = True
    Base.metadata.create_all(sync_engine) # создание
    sync_engine.echo = True

# Запрос на вставку(INSERT)(синхронная сессия)
def insert_table_orm():
    with sync_session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        # session.add(worker_bobr) # Отправка в сессию
        # session.add(worker_volk) или...
        session.add_all([worker_bobr, worker_volk])
        session.flush() # Отправляют в БД но не завершает запрос
        session.commit() # Отправляют в БД но звершает запрос

# Запрос на вставку(INSERT)(асинхронная сессия)
async def insert_table():
    async with async_session_factory() as session:
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        # session.add(worker_bobr) # Отправка в сессию
        # session.add(worker_volk) или...
        session.add_all([worker_bobr, worker_volk])
        await session.commit() # Тогда окажутся в БД
def select_workers_orm():
    with sync_session_factory() as session:
        # worker_id = 1
        # worker_bobr = session.get(WorkerOrm, worker_id) # толко 1 работник
        query = select(WorkerOrm) # SELECT * FROM workers;
        res = session.execute(query)
        workers = res.scalars().all() # первое значение из каждой строки
        print(f"{workers=}")

def update_workers_orm(worker_id: int = 2, new_username: str = "Misha"):
    with sync_session_factory() as session:
        worker_volk = session.get(WorkerOrm, worker_id)
        worker_volk.username = new_username 
        session.expire_all() # отменяет изменения со всеми а просто expire(arg) только с тем что в скобках
        session.refresh(worker_volk) # получает самые свежие данные из БД
        session.commit()