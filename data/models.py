from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text, CheckConstraint, Index, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum
from datetime import datetime
from typing import Annotated

# Кастомные типы с предустановленными настройками для столбцов
intpk = Annotated[int, mapped_column(primary_key=True)]
creared_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]

# Хранение данных в декларативном стиле (ORM Models)
class WorkerOrm(Base):
    """
    ORM модель для таблицы 'workers'. Представляет строку в таблице как объект Python.
    """
    __tablename__ = "workers" # Название таблицы в базе данных.
    id: Mapped[intpk] # Объявляем столбец 'id' с типом 'intpk' (целое число, первичный ключ).
    username: Mapped[str] # Объявляем столбец 'username' с типом 'str' (строка).
    lastname: Mapped[str] # Объявляем столбец 'lastname' с типом 'str' (строка).
    phone_number: Mapped[int] # Объявляем столбец 'phone_number' с типом 'int'

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        # backref="worker" не рекомендуется
    )
    # Это основное определение отношения "один ко многим" (One-to-Many).
    # - `resumes`: Имя атрибута в классе WorkerOrm, который будет содержать список
    #              всех объектов ResumesOrm, связанных с данным WorkerOrm.
    # - `Mapped[List["ResumesOrm"]]`: Аннотация типа, которая указывает, что `resumes`
    #                                  будет списком (`List`) объектов `ResumesOrm`.
    #                                  Использование строковой ссылки `"ResumesOrm"`
    #                                  помогает избежать ошибок импорта, если ResumesOrm
    #                                  определен после WorkerOrm или в другом файле.
    # - `relationship()`: Функция SQLAlchemy, которая настраивает связь между моделями.
    # - `back_populates="worker"`: Это критически важный аргумент. Он указывает,
    #                               что в связанной модели `ResumesOrm` есть атрибут `worker`,
    #                               который ссылается обратно на этот `WorkerOrm`.
    #                               Это создает двунаправленную связь, позволяя
    #                               эффективно перемещаться между связанными объектами.
    #                               `backref` - это более старый, менее гибкий способ
    #                               достижения того же эффекта, поэтому его не рекомендуют.

    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker",
        # backref="worker" не рекомендуется
        primaryjoin="and_(WorkerOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')",
        order_by="ResumesOrm.id.desc()",
        #lazy="selectin" не рекомендуется
    )
    # Это **кастомное** отношение "один ко многим", которое фильтрует связанные резюме.
    # - `resumes_parttime`: Новый атрибут, который будет содержать ТОЛЬКО резюме
    #                        с типом занятости 'parttime' (неполная занятость).
    # - `Mapped[List["ResumesOrm"]]`: Аннотация типа, как и выше.
    # - `relationship()`: Используется для настройки связи.
    # - `back_populates="worker"`: Здесь также используется `worker` как обратный атрибут.
    #                              Важно отметить, что обе связи (`resumes` и `resumes_parttime`)
    #                              используют один и тот же обратный атрибут `worker` в `ResumesOrm`.
    #                              Это допустимо, но нужно понимать, что атрибут `ResumesOrm.worker`
    #                              будет указывать на общий `WorkerOrm`.
    # - `primaryjoin="and_(WorkerOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')"`:
    #   Это ключевой аргумент, который определяет **условие JOIN** для этой конкретной связи.
    #   Он говорит SQLAlchemy, как соединять таблицы, когда вы запрашиваете `resumes_parttime`.
    #   - `WorkerOrm.id == ResumesOrm.worker_id`: Стандартное условие соединения по внешнему ключу.
    #   - `ResumesOrm.workload == 'parttime'`: **Дополнительное условие**, которое фильтрует
    #                                          резюме, оставляя только те, у которых `workload` равен 'parttime'.
    #   Использование `and_()` из SQLAlchemy позволяет объединять несколько условий.
    #   Это очень мощный инструмент для создания фильтрованных коллекций связанных объектов.


    repr_cols_nums = 3
    repr_cols = ("create_at",)

class Workload(enum.Enum):
    """
    Enum (перечисление) для представления возможных вариантов занятости.
    """
    parttime = "parttime" # Вариант "parttime".
    fulltime = "fulltime" # Вариант "fulltime".

class ResumesOrm(Base):
    """
    ORM модель для таблицы 'resumes'. Представляет строку в таблице как объект Python.
    """
    __tablename__ = "resumes" # Название таблицы в базе данных.
    id: Mapped[intpk] # Объявляем столбец 'id' с типом 'intpk' (целое число, первичный ключ).
    title: Mapped[str_256] # Объявляем столбец 'title' с типом 'str_256' (строка с ограничением длины 256).
    compensation: Mapped[int | None] # Объявляем столбец 'compensation' с типом 'int' или None (может быть NULL в базе).
    workload: Mapped[Workload] # Объявляем столбец 'workload' с типом 'Workload' (наш enum).
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE")) # Объявляем столбец 'worker_id' как внешний ключ, ссылающийся на столбец 'id' таблицы 'workers'.
                                                                                     # 'ondelete="CASCADE"' означает, что при удалении записи из 'workers', все связанные записи в 'resumes' также будут удалены.
    created_at: Mapped[creared_at] # Объявляем столбец 'create_at' с типом 'creare_at' (datetime с дефолтным значением - текущее UTC время на сервере БД).
    updated_at: Mapped[updated_at] # Объявляем столбец 'update_at' с типом 'update_at' (datetime с дефолтным значением - текущее UTC время на сервере БД, обновляется на текущее UTC время при изменении записи ORM).

    worker: Mapped["WorkerOrm"] = relationship(back_populates="resumes")
    # Это определение отношения "многие к одному" (Many-to-One).
    # Оно находится в классе ResumesOrm, потому что **много** резюме
    # могут принадлежать **одному** работнику.

    # - `worker`: Это имя атрибута в классе ResumesOrm. Когда вы получите объект ResumesOrm
    #             из базы данных, этот атрибут будет содержать связанный объект WorkerOrm,
    #             которому принадлежит это резюме.
    #             Например, если у вас есть `resume_obj`, вы можете получить связанного работника
    #             просто обратившись к `resume_obj.worker`.

    # - `Mapped["WorkerOrm"]`: Это подсказка типа (type hint), которая используется SQLAlchemy
    #                          и статическими анализаторами кода. Она указывает, что атрибут `worker`
    #                          ожидается быть объектом типа WorkerOrm.
    #                          Использование строковой ссылки `"WorkerOrm"` является общепринятой практикой
    #                          для предотвращения ошибок импорта, если WorkerOrm еще не был определен
    #                          (или находится в другом файле и создает циклическую зависимость).

    # - `relationship(back_populates="resumes")`: Это ключевая функция SQLAlchemy, которая настраивает саму связь.
    #   - `back_populates="resumes"`: Этот аргумент устанавливает двунаправленную связь.
    #     Он говорит SQLAlchemy, что в связанной модели WorkerOrm существует атрибут
    #     с именем `resumes` (как правило, это `Mapped[list["ResumesOrm"]]`),
    #     который ссылается обратно на этот список резюме.
    #     Когда вы устанавливаете или изменяете `resume_obj.worker`, SQLAlchemy автоматически
    #     обновляет соответствующий список `worker_obj.resumes` и наоборот,
    #     обеспечивая согласованность данных в обоих направлениях.

    vacancies_replied: Mapped[list["VacanciesOrm"]] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replice",
    )


    repr_cols_nums = 9
    repr_cols = ("create_at")

    __table_args__ = (
        # PrimaryKeyConstraint("id"),
        # Этот аргумент `__table_args__` используется в SQLAlchemy ORM для определения
        # дополнительных конфигураций на уровне таблицы, таких как индексы,
        # ограничения (constraints) и другие специфичные для базы данных опции.
        # Он принимает кортеж (tuple) с этими конфигурациями.

        # PrimaryKeyConstraint("id"),
        # Закомментированная строка.
        # `PrimaryKeyConstraint("id")` явно указывает, что столбец "id" является первичным ключом.
        # В большинстве случаев это избыточно, так как `Column("id", Integer, primary_key=True)`
        # или `id: Mapped[intpk]` уже объявляют столбец как первичный ключ,
        # и SQLAlchemy автоматически создает соответствующее ограничение.
        # Может быть полезно для составных первичных ключей или для явного контроля.

        Index("title_index", "title"),
        # `Index("title_index", "title")` создает индекс для столбца "title".
        # - "title_index": Это имя, которое будет присвоено индексу в базе данных.
        #                  Имена индексов должны быть уникальными в пределах таблицы.
        # - "title": Это имя столбца, по которому будет создан индекс.
        # Зачем нужен индекс?
        # Индексы значительно ускоряют операции поиска (SELECT), сортировки (ORDER BY) и фильтрации (WHERE)
        # по индексированным столбцам, поскольку база данных может быстрее находить нужные данные,
        # не просматривая всю таблицу. Это как алфавитный указатель в книге.

        CheckConstraint("compensation > 0", name="check_compens_positive"),
        # `CheckConstraint("compensation > 0", name="check_compens_positive")` создает ограничение проверки.
        # - "compensation > 0": Это SQL-выражение, которое должно быть истинным для каждой строки в таблице.
        #                       В данном случае, оно гарантирует, что значение в столбце "compensation"
        #                       всегда будет больше нуля. Если вы попытаетесь вставить или обновить строку
        #                       со значением `compensation`, которое меньше или равно нулю, база данных
        #                       выдаст ошибку.
        # - `name="check_compens_positive"`: Это имя, которое будет присвоено ограничению в базе данных.
        #                                     Полезно для отладки и управления ограничениями.
        # Зачем нужны ограничения проверки?
        # Они обеспечивают целостность данных на уровне базы данных, гарантируя, что данные
        # соответствуют определенным правилам до их сохранения. Это помогает предотвратить
        # вставку недействительных или некорректных данных в таблицу.
    )

class VacanciesOrm(Base):
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]

    resumes_replied: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replice",
    )

class VacanciesReplioceOrm(Base):
    __tablename__ = "vacancies_replice"

    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True,
    )

    cover_letter: Mapped[str | None]


# Хранение всех данных в императивном стиле (Core API)
metadata_obj = MetaData() # Создаем объект MetaData для хранения информации о схеме базы данных.

# Объявление таблицы 'workers' в императивном стиле
workers_table = Table(
    "workers", # Название таблицы.
    metadata_obj, # Связываем таблицу с нашим объектом MetaData.
    Column("id", Integer, primary_key=True), # Определяем столбец 'id': имя - "id", тип данных - Integer, является первичным ключом.
    Column("username", String) # Определяем столбец 'username': имя - "username", тип данных - String (текст).
)
