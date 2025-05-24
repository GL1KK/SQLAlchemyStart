from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

# Абсолютные импорты ваших модулей
from queries.core import create_table_core, insert_data_core, select_workers_core, update_workers_core
from queries.orm import (
    create_table_orm,
    insert_table_orm,
    select_workers_orm,
    select_resumes_avg_compensation,
    join_cte_subquery_window_func,
    select_workers_with_lazy_relationship,
    select_workers_with_joined_relationship,
    select_workers_with_selectin_relationship,
    select_workers_with_condition_relationship,
    select_workers_with_condition_relationship_containseager,
    select_workers_with_condition_relationship_containseager_limit,
    Pydantic_DTO_only_select,
    Pydantic_DTO_relationship,
    Pydantic_DTO_join,
    select_resumes_with_all_relationships,
    add_vacansies_and_replice
)

# Вызовы функций для демонстрации (если вы хотите запускать их при старте приложения)
# create_table_orm()
# insert_table_orm()
# select_workers_orm()
# select_resumes_avg_compensation()
# asyncio.run(join_cte_subquery_window_func()) # Убедитесь, что join_cte_subquery_window_func действительно асинхронна
# select_workers_with_lazy_relationship()
# select_workers_with_joined_relationship()
# select_workers_with_selectin_relationship()
# select_workers_with_condition_relationship()
# select_workers_with_condition_relationship_containseager()
# select_workers_with_condition_relationship_containseager_limit()
# Pydantic_DTO_only_select()
# Pydantic_DTO_relationship()
# Pydantic_DTO_join()
# select_resumes_with_all_relationships()
# add_vacansies_and_replice()
# def create_fastapi_app():
#     app = FastAPI()
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"]
#     )
#     @app.get("/workers")
#     async def get_workers():
#         # Обратите внимание: Pydantic_DTO_relationship() - это, скорее всего, функция, которая возвращает данные
#         # Если это класс DTO, то вам нужно будет передать в него данные, полученные из БД.
#         workers = Pydantic_DTO_relationship() # Вам нужно получить реальные данные здесь
#         return workers
#     @app.get("/resumes")
#     async def get_resumes():
#         # Обратите внимание: Pydantic_DTO_relationship() - это, скорее всего, функция, которая возвращает данные
#         # Если это класс DTO, то вам нужно будет передать в него данные, полученные из БД.
#         resumes = select_resumes_with_all_relationships() # Вам нужно получить реальные данные здесь
#         return resumes
#     return app

# app = create_fastapi_app()
