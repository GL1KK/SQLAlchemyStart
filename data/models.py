from sqlalchemy import Table, Column, Integer, String, MetaData

# Хранение всех данных
metadata_obj = MetaData()

# Обьявление таблицы
workers_table = Table(
    "workers", # Название
    metadata_obj, # данные
    Column("id", Integer, primary_key=True), # Создание столбца 1 - имя, 2 - тип данных, 3 - первичный ключ
    Column("username", String) 
)