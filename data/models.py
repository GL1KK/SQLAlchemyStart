from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
import enum
import datetime
from typing import Annotated

# Кастомный тип
intpk = Annotated[int, mapped_column(primary_key=True)] 
creare_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
update_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow)]

# Хранение данных в декларативном стиле(мне так удобнее)
class WorkerOrm(Base):
    __tablename__ = "workers" # Название
    id: Mapped[intpk] # = mapped_column(primary_key=True) # Создание столбца
    username: Mapped[str] # = mapped_column() опоцианально

class Workload(enum.Enum): # Создаем enum 
    parttime = "parttime" # Обьекты enum
    fulltime = "fulltime"

class ResumesOrm(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_256]
    copensation: Mapped[int | None] # = mapped_column(nullable=True) Не обязательное поле. Или так или так
    workload: Mapped[Workload] # тип данных Wokload
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE")) # внешний ключ для связи указываем название таблицы и столбец или (WorkerOrm.id), ondelete="CASCADE" удаляет все связанное с пользователем
    create_at: Mapped[creare_at] #= mapped_column(server_default=text("TIMEZONE('utc', now())")) # дефолтное что должно добавится в БД, func.now местное время, TIMEZONE время utc
    update_at: Mapped[update_at] #= mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow) # Обнавляется при изменении ТОЛЬКО С ORM


# Хранение всех данных в императивном стиле
metadata_obj = MetaData()

# Обьявление таблицы
workers_table = Table(
    "workers", # Название
    metadata_obj, # данные
    Column("id", Integer, primary_key=True), # Создание столбца 1 - имя, 2 - тип данных, 3 - первичный ключ
    Column("username", String) 
)