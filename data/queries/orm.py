from sqlalchemy import text, insert, select, func, cast, Integer, and_
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from database import sync_engine, async_engine, sync_session_factory, async_session_factory, Base
from models import metadata_obj, WorkerOrm, ResumesOrm, Workload, VacanciesOrm, VacanciesReplioceOrm
from datetime import datetime
from schemas import *
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
        worker_bobr = WorkerOrm(username="Bobr", lastname="Kurwa", phone_number=790)
        worker_volk = WorkerOrm(username="Volk", lastname="Makaka", phone_number=890)
        worker_lisa = WorkerOrm(username="Lisa", lastname="Joinova", phone_number=659)
        worker_misa = WorkerOrm(username="Misa", lastname="Light", phone_number=795)
        worker_light = WorkerOrm(username="Light", lastname="Misa", phone_number=790)
        worker_sany = WorkerOrm(username="Sany", lastname="Lala", phone_number=123)
        # Добавляем все созданные экземпляры работников в сессию.
        session.add_all([worker_bobr, worker_volk, worker_lisa, worker_misa, worker_light, worker_sany])
        session.commit() # Фиксируем транзакцию, отправляя данные в базу данных.
        # Создаем экземпляры модели ResumesOrm для добавления резюме.
        # Связываем каждое резюме с соответствующим работником по его ID (worker_id).
        resumes_bobr = ResumesOrm(title="Bobr.... Python", compensation=100000,
            workload=Workload.fulltime, worker_id=worker_bobr.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        resumes_volk = ResumesOrm(title="Volk.... Python", compensation=150000,
            workload=Workload.parttime, worker_id=worker_volk.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        resumes_lisa = ResumesOrm(title="lisa.... python", compensation=200000,
            workload=Workload.parttime, worker_id=worker_lisa.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        resumes_misa = ResumesOrm(title="Misa.... Python", compensation=225000,
            workload=Workload.fulltime, worker_id=worker_misa.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        resumes_light = ResumesOrm(title="Lihht.... Python", compensation=50000,
            workload=Workload.fulltime, worker_id=worker_light.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        resumes_sany = ResumesOrm(title="Sany.... python", compensation=230000,
            workload=Workload.parttime, worker_id=worker_sany.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
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
def select_workers_with_lazy_relationship():
    """
    Эта функция демонстрирует ленивую (lazy) загрузку связанных данных.

    **Отношение "один ко многим" (One-to-Many):**
    В данном примере `WorkerOrm` имеет отношение "один ко многим" с `ResumesOrm`
    (один работник может иметь много резюме). Связь определена в `WorkerOrm`
    через `relationship("ResumesOrm", back_populates="worker")` и в `ResumesOrm`
    через `relationship("WorkerOrm", back_populates="resumes")` и `ForeignKey("workers.id")`.

    При ленивой загрузке, когда вы запрашиваете `WorkerOrm`, связанные `ResumesOrm`
    не загружаются немедленно. Они будут загружены отдельным SQL-запросом
    только при первом обращении к атрибуту `resumes` объекта `WorkerOrm`.

    **Подходит для:**
    - Случаев, когда связанные данные нужны не всегда.
    - Экономии ресурсов при выборке большого количества основных сущностей,
      если связанные данные нужны лишь для небольшой их части.
    - Может привести к проблемам производительности ("N+1 запрос"), если вам
      нужно получить связанные данные для большого количества основных сущностей.
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        query = (
            select(WorkerOrm) # Создаем запрос на выборку всех работников из таблицы 'workers'.
        )

        res = session.execute(query) # Выполняем запрос на выборку работников и получаем объект Result.
        result = res.scalars().all() # Извлекаем все объекты WorkerOrm из объекта Result в виде списка.

        # На данный момент связанные резюме (отношение 'resumes') для каждого работника
        # еще НЕ загружены из базы данных. SQLAlchemy знает о связи, но данные не подгружены.

        worker_1_resumes = result[0].resumes # Вот здесь, при первом обращении к атрибуту 'resumes' первого работника,
                                             # SQLAlchemy автоматически выполнит дополнительный SQL-запрос
                                             # (если сессия еще активна и данные не были загружены ранее)
                                             # чтобы загрузить все связанные с этим работником резюме.

        print(f"{worker_1_resumes}") # Выводим список объектов ResumesOrm, связанных с первым работником.

        worker_2_resumes = result[1].resumes # Аналогично, при первом обращении к атрибуту 'resumes' второго работника,
                                             # будет выполнен еще один отдельный SQL-запрос для загрузки его резюме.

        print(f"{worker_2_resumes}") # Выводим список объектов ResumesOrm, связанных со вторым работником.

def select_workers_with_condition_relationship():
    """
    Эта функция демонстрирует жадную (eager) загрузку связанных данных
    для **специально отфильтрованной коллекции** (resumes_parttime) с использованием `selectinload`.

    Здесь мы используем отношение `WorkerOrm.resumes_parttime`, которое уже
    предварительно настроено в модели `WorkerOrm` с условием `primaryjoin`
    для выбора только резюме с `workload == 'parttime'`.
    `selectinload` загрузит эти отфильтрованные резюме отдельным запросом после
    основного запроса к работникам.

    **Подходит для:**
    - Загрузки коллекций, которые уже отфильтрованы на уровне определения отношения
      в ORM-модели с помощью `primaryjoin`.
    - Избегания "N+1" проблемы для таких отфильтрованных коллекций.
    - Ситуаций, где вам нужна специфическая подмножество связанных объектов для каждого основного объекта.
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        query = (
            select(WorkerOrm) # Создаем запрос на выборку всех работников из таблицы 'workers'.
            .options(selectinload(WorkerOrm.resumes_parttime)) # Указываем SQLAlchemy загрузить связанную коллекцию
                                                               # `resumes_parttime` для каждого `WorkerOrm`.
                                                               # `selectinload` выполнит это двумя запросами:
                                                               # 1. Выборка всех WorkerOrm.
                                                               # 2. Выборка всех ResumesOrm, связанных с этими WorkerOrm
                                                               #    и соответствующих условию workload == 'parttime'
                                                               #    (как определено в primaryjoin отношения).
            #.options(selectinload(WorkerOrm.resumes)) # Много relationship много options все логично
            # Эта закомментированная строка показывает, что вы можете использовать несколько `.options()`
            # для загрузки различных связанных коллекций или объектов в одном запросе.
            # Каждая `.options()` будет применять свою стратегию загрузки (например, joinedload, selectinload)
            # к указанному отношению.
        )

        res = session.execute(query) # Выполняем запрос(ы) и получаем объект Result.
        result = res.scalars().all() # Извлекаем все объекты WorkerOrm из объекта Result в виде списка.
                                     # Поскольку `selectinload` загружает коллекции, `scalars().all()`
                                     # вернет только объекты WorkerOrm, и их коллекции `resumes_parttime`
                                     # уже будут заполнены.

        print(result) # Выводим список объектов WorkerOrm. При обращении к `worker.resumes_parttime`
                      # для каждого объекта, соответствующие отфильтрованные резюме будут доступны.

def select_workers_with_condition_relationship_containseager():
    """
    Эта функция демонстрирует жадную загрузку `contains_eager` для фильтрации
    основных сущностей на основе связанных данных.

    `contains_eager` используется, когда вы выполняете `JOIN` вручную в вашем запросе
    (т.е., используете `.join()`), и хотите, чтобы SQLAlchemy "увидел" связанные данные,
    которые уже были загружены этим `JOIN`'ом, и использовал их для заполнения
    атрибутов отношений в ваших ORM-объектах. Это позволяет вам фильтровать
    основные объекты по связанным данным, при этом "жадно" загружая эти связанные данные.

    **Подходит для:**
    - Фильтрации основных объектов на основе условий в связанных таблицах.
    - Избегания повторной загрузки связанных данных, если они уже были получены через `JOIN`.
    - Более сложных сценариев запросов, где `joinedload` или `selectinload`
      могут быть недостаточно гибкими для фильтрации основной коллекции.
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        query = (
            select(WorkerOrm) # Создаем запрос на выборку всех работников.
            .join(WorkerOrm.resumes) # Явно присоединяем таблицу `resumes` к `workers`.
                                     # Это создает SQL JOIN между WorkerOrm и ResumesOrm.
            .options(contains_eager(WorkerOrm.resumes)) # Сообщаем SQLAlchemy, что атрибут `resumes`
                                                        # на объекте `WorkerOrm` должен быть заполнен
                                                        # данными, которые уже получены в результате `JOIN`.
                                                        # SQLAlchemy не будет выполнять дополнительный запрос для резюме.
            .filter(ResumesOrm.workload == 'parttime') # Применяем фильтр к **связанной таблице ResumesOrm**.
                                                        # Это означает, что будут выбраны только те работники,
                                                        # у которых есть хотя бы одно резюме с `workload == 'parttime'`.
        )

        res = session.execute(query) # Выполняем запрос.
        result = res.unique().scalars().all() # Извлекаем уникальные объекты WorkerOrm.
                                             # `.unique()` важен здесь, потому что `JOIN` может привести к
                                             # дублированию объектов WorkerOrm, если у работника несколько резюме,
                                             # соответствующих фильтру. `scalars()` извлекает только WorkerOrm.

        print(result) # Выводим список объектов WorkerOrm. Для каждого WorkerOrm, его коллекция `resumes`
                      # будет содержать только те резюме, которые соответствовали условию фильтрации
                      # (т.е., 'parttime'), так как `contains_eager` их "перехватил" из JOIN.

def select_workers_with_condition_relationship_containseager_limit():
    """
    Эта функция демонстрирует продвинутое использование `contains_eager`
    в сочетании с подзапросом для ограниченной загрузки связанных коллекций.

    Здесь мы хотим выбрать работников, у которых есть резюме с определенным условием,
    и одновременно ограничить количество связанных резюме, которые будут загружены
    для каждого работника (например, только первые 2 "parttime" резюме).
    Это достигается путем создания коррелированного подзапроса для получения ID
    нужных связанных объектов, а затем использования их в основном запросе с `JOIN`
    и `contains_eager`.

    **Подходит для:**
    - Сложных сценариев, где необходимо выборочно загружать ограниченное количество
      связанных объектов на основе определенных критериев (например, "топ N" связанных объектов).
    - Оптимизации запросов для очень больших связанных коллекций, когда нужна
      лишь часть данных.
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        subq = (
            select(ResumesOrm.id.label("parttime_resumes_id")) # Выбираем только ID резюме.
            .filter(ResumesOrm.worker_id == WorkerOrm.id) # **Корреляция:** Этот фильтр связывает подзапрос с внешним запросом.
                                                         # Он означает "для каждого работника во внешнем запросе,
                                                         # выбери резюме, где `worker_id` равен `id` этого работника".
            .order_by(WorkerOrm.id.desc()) # Сортируем резюме (по ID работника в данном случае).
            .limit(2) # Ограничиваем количество выбранных резюме до 2 для каждого работника.
            .scalar_subquery() # Преобразует этот запрос в скалярный подзапрос, который возвращает одно значение.
                               # В данном случае, это будет использоваться в IN-условии,
                               # поэтому он возвращает набор ID.
            .correlate(WorkerOrm) # Явно указывает SQLAlchemy, что этот подзапрос коррелирует с WorkerOrm.
                                 # Это означает, что подзапрос будет выполняться для каждой строки
                                 # из основного запроса WorkerOrm.
        )
        query = (
            select(WorkerOrm) # Выбираем работников.
            .join(ResumesOrm, ResumesOrm.id.in_(subq)) # Соединяем WorkerOrm с ResumesOrm,
                                                       # но условие соединения использует наш подзапрос:
                                                       # присоединяются только те резюме, ID которых
                                                       # были выбраны в `subq` (т.е., первые 2 parttime резюме).
            .options(contains_eager(WorkerOrm.resumes)) # Говорим SQLAlchemy, что `resumes`
                                                        # уже загружены этим `JOIN`'ом
                                                        # и должны быть заполнены.
        )

        res = session.execute(query) # Выполняем запрос.
        result = res.unique().scalars().all() # Извлекаем уникальные объекты WorkerOrm,
                                             # их коллекции `resumes` будут содержать
                                             # только те 2 ограниченных резюме,
                                             # которые были получены через `JOIN`.
        print(result) # Выводим список WorkerOrm с их ограниченными связанными резюме.

def select_workers_with_joined_relationship():
    """
    Эта функция демонстрирует жадную (eager) загрузку связанных данных с помощью joinedload.

    **Отношение "один ко многим" (One-to-Many):**
    Как и в ленивой загрузке, здесь также рассматривается отношение "один ко многим"
    между `WorkerOrm` и `ResumesOrm`.

    При использовании `joinedload(WorkerOrm.resumes)`, SQLAlchemy выполнит один SQL-запрос
    с использованием `JOIN` (обычно `LEFT OUTER JOIN`) для загрузки как информации о работниках,
    так и всех их связанных резюме. Когда вы обращаетесь к атрибуту `resumes` объекта `WorkerOrm`,
    данные уже будут доступны в памяти, и дополнительный запрос не потребуется.

    **Подходит для:**
    - Случаев, когда вам часто нужны связанные данные вместе с основной сущностью.
    - Предотвращения проблемы "N+1 запрос" и повышения производительности,
      когда вы обрабатываете большое количество основных сущностей и их связей.
    - Может привести к избыточной загрузке данных, если связанные данные нужны не для всех
      обрабатываемых основных сущностей.
      Подходит для one to one(o2o(один к одному)) и many to one(m2o(многие к одному))
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        query = (
            select(WorkerOrm) # Создаем запрос на выборку всех работников из таблицы 'workers'.
            .options(joinedload(WorkerOrm.resumes)) # Указываем SQLAlchemy, что отношение 'resumes' должно быть загружено
                                                   # "жадно" (eagerly) с использованием `JOIN`.
        )

        res = session.execute(query) # Выполняем запрос. SQLAlchemy уже загрузил связанные резюме.
        result = res.unique().scalars().all() # Извлекаем уникальные объекты WorkerOrm из результата запроса.
                                             # `.unique()` используется здесь, чтобы избежать дублирования объектов WorkerOrm
                                             # в случае, если у одного работника несколько резюме (из-за JOIN).

        # На данный момент связанные резюме (отношение 'resumes') для каждого работника
        # УЖЕ загружены из базы данных вместе с информацией о работниках.

        worker_1_resumes = result[0].resumes # Доступ к атрибуту 'resumes' первого работника не требует
                                             # выполнения дополнительного SQL-запроса, так как данные уже загружены.

        print(f"{worker_1_resumes}") # Выводим список объектов ResumesOrm, связанных с первым работником.

        worker_2_resumes = result[1].resumes # Аналогично, доступ к атрибуту 'resumes' второго работника также не вызывает
                                             # дополнительного обращения к базе данных.

        print(f"{worker_2_resumes}") # Выводим список объектов ResumesOrm, связанных со вторым работником.

def select_workers_with_selectin_relationship():
    """
    Эта функция демонстрирует жадную (eager) загрузку связанных данных с помощью selectinload.

    **Отношение "один ко многим" (One-to-Many):**
    Как и в предыдущих примерах, здесь также рассматривается отношение "один ко многим"
    между `WorkerOrm` и `ResumesOrm`.

    При использовании `selectinload(WorkerOrm.resumes)`, SQLAlchemy сначала выполняет
    один запрос для получения всех объектов `WorkerOrm`. Затем, SQLAlchemy выполняет
    отдельный SQL-запрос (используя оператор `IN`) для получения всех связанных
    объектов `ResumesOrm` для всех загруженных `WorkerOrm` за один раз.

    **Подходит для:**
    - Предотвращения проблемы "N+1 запрос" с потенциально лучшей производительностью,
      чем `joinedload` в случаях, когда количество связанных записей велико,
      или когда стратегия `JOIN` может быть неоптимальной.
    - Может быть более эффективным, чем `joinedload` для больших коллекций связанных объектов,
      так как позволяет базе данных лучше оптимизировать запрос с `IN`.

    **Как работает:**
    1. Выбираются все работники (`SELECT * FROM workers`).
    2. Собираются ID всех полученных работников.
    3. Выполняется второй запрос (`SELECT * FROM resumes WHERE resumes.worker_id IN (:worker_ids)`),
       где `:worker_ids` - это список ID всех полученных работников.
    4. SQLAlchemy затем сопоставляет полученные резюме с соответствующими работниками в памяти.
    Подходит для one to many(o2m(один ко многим)) и many to many(m2m(многие ко многим))
    """
    with sync_session_factory() as session: # Создаем сессию для взаимодействия с базой данных.
        query = (
            select(WorkerOrm) # Создаем запрос на выборку всех работников из таблицы 'workers'.
            .options(selectinload(WorkerOrm.resumes)) # Указываем SQLAlchemy, что отношение 'resumes' должно быть загружено
                                                     # "жадно" (eagerly) с использованием `SELECT IN`.
        )

        res = session.execute(query) # Выполняем запрос на выборку работников.
        result = res.unique().scalars().all() # Извлекаем уникальные объекты WorkerOrm из результата запроса.

        # На данный момент связанные резюме (отношение 'resumes') для всех работников
        # УЖЕ загружены в память с помощью отдельного запроса с оператором IN.

        worker_1_resumes = result[0].resumes # Доступ к атрибуту 'resumes' первого работника не требует
                                             # дополнительного SQL-запроса, так как данные уже загружены.

        print(f"{worker_1_resumes}") # Выводим список объектов ResumesOrm, связанных с первым работником.

        worker_2_resumes = result[1].resumes # Аналогично, доступ к атрибуту 'resumes' второго работника также не вызывает
                                             # дополнительного обращения к базе данных.

        print(f"{worker_2_resumes}") # Выводим список объектов


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

def Pydantic_DTO_only_select():
    with sync_session_factory() as session:
        query = (
            select(WorkerOrm)
        )
        res = session.execute(query)
        result_orm = res.scalars().all()
        print(f"{result_orm=}")
        result_dto = [WorkersDTO.model_validate(row, from_attributes=True) for row in result_orm]
        print(f"{result_dto=}")

def Pydantic_DTO_relationship():
     with sync_session_factory() as session:
        query = (
            select(WorkerOrm)
            .options(selectinload(WorkerOrm.resumes))
            .limit(2)
        )
        res = session.execute(query)
        result_orm = res.scalars().all()
        print(f"{result_orm=}")
        result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
        print(f"{result_dto=}")
        return result_dto

def Pydantic_DTO_join():
      with sync_session_factory() as session: # Создаем контекстный менеджер для синхронной сессии.
        query = (
            select(
                ResumesOrm.workload, # Получаем столбец 'workload' (тип занятости: fulltime/parttime).
                cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"), # Вычисляем среднюю компенсацию и приводим к целому числу, даем псевдоним 'avg_compensation'.
            )
            .filter(
                and_(
                    ResumesOrm.title.contains("Python"), # Фильтруем резюме, где в заголовке встречается указанный язык (like_language). Оператор 'contains' эквивалентен SQL LIKE %value%.
                    ResumesOrm.compensation > 40000 # Дополнительно фильтруем резюме с компенсацией больше 40000.
                ) # 'and_' используется для объединения нескольких условий фильтрации с логическим "И".
            ) # 'filter' применяет условия отбора к запросу.
            .group_by(ResumesOrm.workload) # Группируем результаты по столбцу 'workload', чтобы вычислить среднюю зарплату для каждой группы (fulltime и parttime).
            .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000) # Применяем фильтр к сгруппированным результатам. Оставляем только те группы, где средняя зарплата больше 70000.
        )
        print(query.compile(compile_kwargs={"literal_binds": True})) # Печатаем скомпилированный SQL-запрос с подставленными значениями для лучшего понимания.
        res = session.execute(query) # Выполняем SQL-запрос и получаем результат.
        result_orm = res.all() # Извлекаем все строки результата. Каждая строка будет содержать 'workload' и 'avg_compensation'.
        print(f"{result_orm=}")
        result_dto = [WorkloadAvgCompensationDTO.model_validate(row, from_attributes=True) for row in result_orm]
        print(f"{result_dto=}")
        return result_dto
      
def add_vacansies_and_replice():
    """
    Эта функция демонстрирует создание новой вакансии и связывание её с
    существующими резюме через отношение "многие ко многим".
    Она имитирует ситуацию, когда резюме "откликаются" на вакансию.
    """
    with sync_session_factory() as session: # Открываем синхронную сессию для взаимодействия с БД.
        # Создаем новый объект вакансии.
        new_vacany = VacanciesOrm(title="Python Developer", compensation=100000)

        # Получаем существующие резюме по их ID.
        # Это необходимо, чтобы установить связь с уже имеющимися объектами в БД.
        resume_1 = session.get(ResumesOrm, 1) # Получаем резюме с ID = 1.
        resume_2 = session.get(ResumesOrm, 2) # Получаем резюме с ID = 2.

        # Если резюме были найдены, добавляем новую вакансию в их коллекцию 'vacancies_replied'.
        # SQLAlchemy автоматически управляет связыванием через промежуточную таблицу для отношения "многие ко многим".
        if resume_1: # Проверяем, что резюме с ID 1 существует.
            resume_1.vacancies_replied.append(new_vacany) # Добавляем новую вакансию к резюме 1.
        else:
            print("Резюме с ID 1 не найдено.")

        if resume_2: # Проверяем, что резюме с ID 2 существует.
            resume_2.vacancies_replied.append(new_vacany) # Добавляем новую вакансию к резюме 2.
        else:
            print("Резюме с ID 2 не найдено.")

        session.commit() # Фиксируем изменения в базе данных.
                         # Это сохранит новую вакансию и обновит связи "многие ко многим".
        print("Новая вакансия добавлена и связана с резюме.")


def select_resumes_with_all_relationships():
    """
    Эта функция демонстрирует продвинутую жадную загрузку связанных данных
    для объекта 'ResumesOrm', включая:
    - `joinedload` для отношения "многие к одному" (Many-to-One) с 'WorkerOrm'.
    - `selectinload` для отношения "многие ко многим" (Many-to-Many) с 'VacanciesOrm',
      с использованием `load_only` для частичной загрузки столбцов из 'VacanciesOrm'.

    Подходит для ситуаций, когда вам нужны все связанные данные сразу,
    и вы хотите оптимизировать количество SQL-запросов.
    """
    with sync_session_factory() as session: # Открываем синхронную сессию для взаимодействия с БД.
        query = (
            select(ResumesOrm) # Создаем запрос на выборку всех резюме.
            # 1. Жадная загрузка Worker (отношение Many-to-One):
            # `joinedload(ResumesOrm.worker)` выполнит JOIN с таблицей 'workers'
            # в основном SQL-запросе, чтобы загрузить данные работника вместе с резюме.
            # Это позволяет избежать "N+1" проблемы для 'worker', так как данные уже есть.
            .options(joinedload(ResumesOrm.worker))

            # 2. Жадная загрузка связанных Vacancies (отношение Many-to-Many) с частичной загрузкой:
            # `selectinload(ResumesOrm.vacancies_replied)` выполнит второй SQL-запрос
            # (после основного запроса на резюме) с использованием оператора `IN` для
            # загрузки всех связанных вакансий.
            # `.load_only(VacanciesOrm.title)` - это важная оптимизация:
            # она указывает SQLAlchemy загружать ТОЛЬКО столбец 'title' из таблицы 'vacancies'
            # для связанных объектов 'VacanciesOrm'. Это уменьшает объем данных,
            # передаваемых по сети, если вам не нужны все столбцы вакансии.
            .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title))
        )
        res = session.execute(query) # Выполняем SQL-запрос(ы).
        # `unique()` используется, чтобы избежать дублирования объектов ResumesOrm,
        # если JOIN с VacanciesOrm приводит к повторениям (например, если у резюме много откликов).
        # `scalars().all()` извлекает все уникальные объекты ResumesOrm.
        result_orm = res.unique().scalars().all()
        print(f"{result_orm=}") # Выводим список полученных объектов ResumesOrm (включая загруженные отношения).

        # Преобразуем полученные ORM-объекты в DTO (Data Transfer Objects) с помощью Pydantic.
        # `from_attributes=True` позволяет Pydantic читать данные напрямую из атрибутов ORM-объекта,
        # включая связанные объекты и коллекции.
        result_dto = [ResumesRelVacanciesReokiedDTO.model_validate(row, from_attributes=True) for row in result_orm]
        print(f"{result_dto}") # Выводим список DTO.

        return result_dto # Возвращаем список DTO для дальнейшего использования.
