from sqlalchemy import text, insert, select, update
from ..database import async_engine, sync_engine
from ..models import metadata_obj, workers_table
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, insert, select, update, text
# Запрос (синхронный)
def get_sync_vers():
    """
    Эта функция выполняет синхронный SQL-запрос для получения версии базы данных
    и выводит результат.
    """
    with sync_engine.connect() as conn: # Устанавливаем синхронное соединение с базой данных.
        # Получаем версию базы данных, используя сырой SQL-запрос (text необходим для выполнения произвольного SQL).
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.first()=}") # Выводим первую строку результата (обычно версия).

# Автокоммит (пример закомментирован)
# with sync_engine.begin() as conn:
#     # получаем версию(без text не работает)
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res}")
# Комментарий к закомментированному блоку:
# Этот блок демонстрирует использование контекстного менеджера sync_engine.begin(),
# который автоматически начинает транзакцию. Однако, в SQLite автокоммит включен по умолчанию,
# поэтому явное управление транзакциями может быть не всегда необходимо для простых операций.
# Для других СУБД (например, PostgreSQL) использование begin() является важной практикой
# для обеспечения целостности данных.

# Запрос (асинхронный)
async def get_async_123():
    """
    Эта асинхронная функция выполняет асинхронный SQL-запрос для получения набора чисел
    и выводит результат.
    """
    async with async_engine.connect() as conn: # Устанавливаем асинхронное соединение с базой данных.
        # Выполняем сырой SQL-запрос для получения двух наборов чисел с помощью UNION.
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}") # Выводим все строки результата.

# Создание таблицы
def create_table_core():
    """
    Эта функция удаляет существующую таблицу 'workers' (если она есть)
    и затем создает таблицу 'workers' на основе определения в metadata_obj.
    """
    sync_engine.echo = False # Отключаем вывод SQL-запросов перед операциями создания/удаления.
    metadata_obj.drop_all(sync_engine) # Удаляем все таблицы, связанные с metadata_obj, из базы данных.
    print("Таблица удалена")
    metadata_obj.create_all(sync_engine) # Создаем все таблицы, определенные в metadata_obj, в базе данных.
    print("Таблица создана")
    sync_engine.echo = True # Включаем вывод SQL-запросов обратно.

# Запрос на вставку данных (INSERT)
def insert_data_core():
    """
    Эта функция выполняет SQL-запрос для вставки данных в таблицу 'workers'
    с использованием Core API SQLAlchemy.
    """
    with sync_engine.connect() as conn: # Устанавливаем синхронное соединение с базой данных.
        # stmt = """INSERT INTO workers (username)  VALUES # ТАК НЕ НАДА
        # ('Bobr'),
        # ('Volk');"""
        # Комментарий к неправильному способу:
        # Использование f-строк или конкатенации строк для создания SQL-запросов
        # может привести к SQL-инъекциям и является небезопасной практикой.

        # Правильный способ вставки данных с использованием Core API:
        stmt = insert(workers_table).values([ # Создаем объект запроса INSERT для таблицы 'workers' и указываем значения для вставки.
            {"username": "Bobr"}, # Первая строка данных для вставки (словарь: столбец -> значение).
            {"username": "Volk"}  # Вторая строка данных для вставки.
        ])
        conn.execute(stmt) # Выполняем SQL-запрос на вставку.
        conn.commit() # Фиксируем транзакцию, сохраняя изменения в базе данных.

# Запрос на выборку данных (SELECT)
def select_workers_core():
    """
    Эта функция выполняет SQL-запрос для выборки всех данных из таблицы 'workers'
    с использованием Core API SQLAlchemy и выводит результат.
    """
    with sync_engine.connect() as conn: # Устанавливаем синхронное соединение с базой данных.
        query = select(workers_table) # Создаем объект запроса SELECT для таблицы 'workers' (эквивалентно SELECT * FROM workers;).
        res = conn.execute(query) # Выполняем SQL-запрос на выборку.
        workers = res.all() # Получаем все строки результата. Каждая строка представляет собой кортеж со значениями столбцов.
        print(workers) # Выводим полученные строки.

# Запрос на обновление данных (UPDATE)
def update_workers_core(worker_id: int = 2, new_username: str = "Misha"):
    """
    Эта функция выполняет SQL-запрос для обновления имени пользователя в таблице 'workers'
    для записи с указанным ID, используя Core API SQLAlchemy.
    """
    with sync_engine.connect() as conn: # Устанавливаем синхронное соединение с базой данных.
        # stmt = text("UPDATE workers SET username={new_username}") # SQL иньекция так нельза!!!!
        # Комментарий к небезопасному способу:
        # Нельзя напрямую подставлять значения в SQL-запросы с помощью f-строк,
        # так как это делает код уязвимым для SQL-инъекций.

        # stmt = text("UPDATE workers SET username=:username WHERE id=:id") # Правильно(сырой запрос)
        # stmt = stmt.bindparams(username=new_username, id=workers_id)
        # Комментарий к безопасному сырому запросу:
        # Использование плейсхолдеров (:) и bindparams() является безопасным способом
        # передачи параметров в сырые SQL-запросы.

        # Более удобный способ обновления с использованием Core API:
        stmt = update(workers_table).values(username=new_username).filter_by(id=worker_id) # Создаем объект запроса UPDATE, указываем новые значения и условие WHERE (filter_by эквивалентен WHERE id=:id).
        # where/filter(workers_table.c.id==workers_id) не оч
        # Комментарий к альтернативному способу условия WHERE:
        # Можно использовать метод where() или filter() с условием, обращающимся к столбцу таблицы (workers_table.c.id).
        # filter_by() является более лаконичным способом для простых условий равенства по первичному ключу или другим столбцам.
        conn.execute(stmt) # Выполняем SQL-запрос на обновление.
        conn.commit() # Фиксируем транзакцию, сохраняя изменения в базе данных.