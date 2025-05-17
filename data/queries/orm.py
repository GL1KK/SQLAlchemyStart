from sqlalchemy import text, insert, select, func, cast, Integer, and_
from sqlalchemy.orm import aliased
from database import sync_engine, async_engine, sync_session_factory, async_session_factory, Base
from models import metadata_obj, WorkerOrm, ResumesOrm, Workload
import datetime
# Функция для создания таблиц в базе данных
def create_table_orm():
    """
    Эта функция удаляет все существующие таблицы, включает вывод SQL-запросов
    и создает все таблицы, определенные в метаданных Base.
    """
    Base.metadata.drop_all(sync_engine) # Удаляет все таблицы, определенные в Base.metadata из базы данных.
    sync_engine.echo = True # Включает вывод сгенерированных SQL-запросов в консоль.
    Base.metadata.create_all(sync_engine) # Создает все таблицы, определенные в Base.metadata в базе данных.
    sync_engine.echo = True # Включает вывод сгенерированных SQL-запросов в консоль (повторно).
    print("ready") # Выводит сообщение об успешном завершении создания таблиц.

# Запрос на вставку данных в таблицы (синхронная сессия)
def insert_table_orm():
    """
    Эта функция создает и добавляет несколько записей в таблицы 'workers' и 'resumes'
    с использованием синхронной сессии SQLAlchemy. Затем она фиксирует изменения в базе данных.
    """
    with sync_session_factory() as session: # Создаем контекстный менеджер для синхронной сессии. Сессия автоматически закроется после выполнения блока.
        # Создаем экземпляры модели WorkerOrm для добавления работников.
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        worker_lisa = WorkerOrm(username="Lisa")
        worker_misa = WorkerOrm(username="Misa")
        worker_light = WorkerOrm(username="Light")
        worker_sany = WorkerOrm(username="Sany")
        # Добавляем все созданные экземпляры работников в сессию.
        session.add_all([worker_bobr, worker_volk, worker_lisa, worker_misa, worker_light, worker_sany])
        session.commit() # Фиксируем транзакцию, отправляя данные в базу данных.
        # Создаем экземпляры модели ResumesOrm для добавления резюме.
        # Связываем каждое резюме с соответствующим работником по его ID (worker_id).
        resumes_bobr = ResumesOrm(title="Bobr.... Python", compensation=100000,
            workload=Workload.fulltime, worker_id=worker_bobr.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        resumes_volk = ResumesOrm(title="Volk.... Python", compensation=150000,
            workload=Workload.parttime, worker_id=worker_volk.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        resumes_lisa = ResumesOrm(title="lisa.... python", compensation=200000,
            workload=Workload.parttime, worker_id=worker_lisa.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        resumes_misa = ResumesOrm(title="Misa.... Python", compensation=225000,
            workload=Workload.fulltime, worker_id=worker_misa.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        resumes_light = ResumesOrm(title="Lihht.... Python", compensation=50000,
            workload=Workload.fulltime, worker_id=worker_light.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        resumes_sany = ResumesOrm(title="Sany.... python", compensation=230000,
            workload=Workload.parttime, worker_id=worker_sany.id, create_at=datetime.datetime.utcnow(), update_at=datetime.datetime.utcnow())
        # session.add(worker_bobr) # Отправка отдельного объекта в сессию (уже сделано через add_all выше).
        # session.add(worker_volk) или... (уже сделано через add_all выше).
        # Добавляем все созданные экземпляры резюме в сессию.
        session.add_all([resumes_bobr,resumes_volk, resumes_lisa, resumes_misa, resumes_light, resumes_sany])
        # session.flush() # Отправляет изменения в базу данных, но не завершает транзакцию (не делает commit).
        session.commit() # Фиксируем транзакцию, сохраняя все изменения в базе данных.

# Запрос на вставку данных в таблицу (асинхронная сессия)
async def insert_table():
    """
    Эта асинхронная функция создает и добавляет несколько записей в таблицу 'workers'
    с использованием асинхронной сессии SQLAlchemy. Затем она асинхронно фиксирует изменения.
    """
    async with async_session_factory() as session: # Создаем контекстный менеджер для асинхронной сессии.
        # Создаем экземпляры модели WorkerOrm для добавления работников.
        worker_bobr = WorkerOrm(username="Bobr")
        worker_volk = WorkerOrm(username="Volk")
        # session.add(worker_bobr) # Отправка отдельного объекта в сессию.
        # session.add(worker_volk) или...
        # Добавляем все созданные экземпляры работников в сессию.
        session.add_all([worker_bobr, worker_volk])
        await session.commit() # Асинхронно фиксируем транзакцию, отправляя данные в базу данных.

# Запрос на выборку данных из таблицы 'workers'
def select_workers_orm():
    """
    Эта функция выполняет запрос на выборку всех записей из таблицы 'workers'
    с использованием синхронной сессии и выводит полученные данные.
    """
    with sync_session_factory() as session: # Создаем контекстный менеджер для синхронной сессии.
        # worker_id = 1
        # worker_bobr = session.get(WorkerOrm, worker_id) # Получает запись работника по его ID (если существует).
        query = select(WorkerOrm) # Создаем SQL-запрос SELECT * FROM workers;.
        res = session.execute(query) # Выполняем SQL-запрос и получаем результат.
        workers = res.scalars().all() # Извлекаем все объекты WorkerOrm из результата запроса.
        print(f"{workers=}") # Выводим список полученных объектов работников.

# Пример функции для обновления данных (закомментирован)
# def update_workers_orm(worker_id: int = 2, new_username: str = "Misha"):
#     with sync_session_factory() as session:
#         worker_volk = session.get(WorkerOrm, worker_id) # Получаем запись работника по его ID.
#         # worker_volk.username = new_username
#         # session.expire_all() # Отменяет все изменения, отслеживаемые сессией.
#         session.refresh(worker_volk) # Получает самые свежие данные из базы данных для данного объекта.
#         session.commit() # Фиксируем изменения в базе данных.

# Запрос на выборку средней зарплаты из таблицы 'resumes' с фильтрацией и группировкой
def select_resumes_avg_compensation(like_language: str = "Python"):
    """
    Эта функция выполняет запрос на выборку средней компенсации из таблицы 'resumes',
    фильтруя по языку в заголовке и минимальной компенсации, группируя по типу занятости
    и фильтруя группы по минимальной средней компенсации.
    """
    with sync_session_factory() as session: # Создаем контекстный менеджер для синхронной сессии.
        query = (
            select(
                ResumesOrm.workload, # Получаем столбец 'workload' (тип занятости: fulltime/parttime).
                cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"), # Вычисляем среднюю компенсацию и приводим к целому числу, даем псевдоним 'avg_compensation'.
            )
            .filter(
                and_(
                    ResumesOrm.title.contains(like_language), # Фильтруем резюме, где в заголовке встречается указанный язык (like_language). Оператор 'contains' эквивалентен SQL LIKE %value%.
                    ResumesOrm.compensation > 40000 # Дополнительно фильтруем резюме с компенсацией больше 40000.
                ) # 'and_' используется для объединения нескольких условий фильтрации с логическим "И".
            ) # 'filter' применяет условия отбора к запросу.
            .group_by(ResumesOrm.workload) # Группируем результаты по столбцу 'workload', чтобы вычислить среднюю зарплату для каждой группы (fulltime и parttime).
            .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000) # Применяем фильтр к сгруппированным результатам. Оставляем только те группы, где средняя зарплата больше 70000.
        )
        print(query.compile(compile_kwargs={"literal_binds": True})) # Печатаем скомпилированный SQL-запрос с подставленными значениями для лучшего понимания.
        res = session.execute(query) # Выполняем SQL-запрос и получаем результат.
        result = res.all() # Извлекаем все строки результата. Каждая строка будет содержать 'workload' и 'avg_compensation'.
        print(result) # Выводим полученный результат.

async def join_cte_subquery_window_func(like_language: str = "Python"):
    """
    Эта асинхронная функция демонстрирует использование CTE (Common Table Expression),
    подзапроса и оконной функции в SQLAlchemy для выборки данных о резюме и работниках.
    Она также вычисляет разницу между компенсацией работника и средней компенсацией
    для его уровня загрузки.
    """

    # Используем асинхронный контекстный менеджер для создания асинхронной сессии.
    async with async_session_factory() as session:
        # Создаем псевдонимы (временные другие имена) для наших таблиц "ResumesOrm" и "WorkerOrm".
        # Это полезно, когда мы соединяем таблицу саму с собой или когда имена таблиц длинные.
        r = aliased(ResumesOrm)
        w = aliased(WorkerOrm)

        # Создаем подзапрос с именем "helper1".
        # Этот подзапрос выбирает данные из таблиц "ResumesOrm" (через псевдоним 'r') и "WorkerOrm" (через псевдоним 'w').
        subq = (
            select(
                r,  # Выбираем все столбцы из таблицы "ResumesOrm" (под псевдонимом 'r').
                w,  # Выбираем все столбцы из таблицы "WorkerOrm" (под псевдонимом 'w').
                w.id.label("worler_id"), # Явно присваиваем псевдоним "worler_id" столбцу 'id' из таблицы 'WorkerOrm'.
                # Используем оконную функцию AVG для вычисления средней компенсации.
                # OVER (PARTITION BY r.workload) означает, что средняя компенсация вычисляется
                # отдельно для каждого уникального значения в столбце "workload" таблицы "ResumesOrm".
                func.avg(r.compensation)
                .over(partition_by=r.workload)
                .cast(Integer)  # Приводим результат средней компенсации к целому числу.
                .label("avg_workload_compensation"),  # Даем этому вычисленному столбцу имя "avg_workload_compensation".
            )
            # Соединяем таблицы "ResumesOrm" ('r') и "WorkerOrm" ('w') по условию,
            # что столбец "worker_id" в "ResumesOrm" равен столбцу "id" в "WorkerOrm".
            .join(r, r.worker_id == w.id)
            .subquery("helper1")  # Превращаем этот запрос в подзапрос и даем ему имя "helper1".
        )

        # Создаем CTE (Common Table Expression) с именем "helper2".
        # CTE - это временный именованный результирующий набор, который можно использовать
        # в одном запросе SELECT, INSERT, UPDATE или DELETE.
        cte = (
            select(
                subq.c.worler_id,  # Выбираем столбец "worler_id" (псевдоним 'id' из 'WorkerOrm') из подзапроса "helper1" (доступ через атрибут 'c').
                subq.c.username,  # Выбираем столбец "username" из подзапроса "helper1".
                subq.c.compensation,  # Выбираем столбец "compensation" из подзапроса "helper1".
                subq.c.workload,  # Выбираем столбец "workload" из подзапроса "helper1".
                subq.c.avg_workload_compensation,  # Выбираем вычисленный столбец "avg_workload_compensation" из подзапроса "helper1".
                # Вычисляем разницу между фактической компенсацией и средней компенсацией для данного уровня загрузки.
                (subq.c.compensation - subq.c.avg_workload_compensation)
                .label("compensation_diff")  # Даем этому вычисленному столбцу имя "compensation_diff".
            )
            .cte("helper2")  # Определяем этот SELECT как CTE с именем "helper2".
        )

        # Создаем основной запрос, который выбирает данные из нашего CTE "helper2".
        query = (
            select(cte)  # Выбираем все столбцы из CTE "helper2".
            .order_by(cte.c.compensation_diff.desc())  # Сортируем результаты по столбцу "compensation_diff" в убывающем порядке (от большего к меньшему).
        )
        res = await session.execute(query) # Асинхронно выполняем SQL-запрос, созданный с помощью SQLAlchemy, и получаем асинхронный объект Result.
        result = res.all() # Асинхронно извлекаем все строки из асинхронного объекта Result. Каждая строка представляет собой кортеж со значениями выбранных столбцов.
        print(result) # Выводим список полученных кортежей.

        # Печатаем скомпилированный SQL-запрос.
        # compile() преобразует запрос SQLAlchemy в SQL-строку.
        # compile_kwargs={"literal_binds": True} заставляет SQLAlchemy вставлять фактические значения
        # вместо параметров-заполнителей, что облегчает чтение сгенерированного SQL.
        # print(query.compile(compile_kwargs={"literal_binds": True}))