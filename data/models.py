from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_256
import enum
import datetime
from typing import Annotated

# Кастомные типы с предустановленными настройками для столбцов
intpk = Annotated[int, mapped_column(primary_key=True)]
creare_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
update_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]

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

    resumes: Mapped[list["ResumesOrm"]] = relationship()
    # Объявляем связь "один ко многим" (One-to-Many) с моделью ResumesOrm.
    # - resumes: Имя атрибута на этом объекте (WorkerOrm), через который будет доступен список связанных объектов ResumesOrm.
    # - Mapped[list["ResumesOrm"]]: Указывает, что атрибут 'resumes' будет списком объектов типа ResumesOrm.
    #   Использование строковой аннотации ("ResumesOrm") помогает избежать проблем
    #   с циклическими импортами, когда модели зависят друг от друга.

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
    create_at: Mapped[creare_at] # Объявляем столбец 'create_at' с типом 'creare_at' (datetime с дефолтным значением - текущее UTC время на сервере БД).
    update_at: Mapped[update_at] # Объявляем столбец 'update_at' с типом 'update_at' (datetime с дефолтным значением - текущее UTC время на сервере БД, обновляется на текущее UTC время при изменении записи ORM).

    worker: Mapped["WorkerOrm"] = relationship()
    # Объявляем связь "многие к одному" (Many-to-One) с моделью WorkerOrm.
    # - worker: Имя атрибута на этом объекте (ResumesOrm), через который будет доступен связанный объект WorkerOrm.
    # - Mapped["WorkerOrm"]: Указывает, что атрибут 'worker' будет объектом типа WorkerOrm.
    #   Аналогично, используется строковая аннотация для предотвращения циклических импортов.

    repr_cols_nums = 4
    repr_cols = ("create_at")



# Хранение всех данных в императивном стиле (Core API)
metadata_obj = MetaData() # Создаем объект MetaData для хранения информации о схеме базы данных.

# Объявление таблицы 'workers' в императивном стиле
workers_table = Table(
    "workers", # Название таблицы.
    metadata_obj, # Связываем таблицу с нашим объектом MetaData.
    Column("id", Integer, primary_key=True), # Определяем столбец 'id': имя - "id", тип данных - Integer, является первичным ключом.
    Column("username", String) # Определяем столбец 'username': имя - "username", тип данных - String (текст).
)