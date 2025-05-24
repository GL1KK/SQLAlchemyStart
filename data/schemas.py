from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from .models import Workload

class WorkersAddDTO(BaseModel):
    username: str

class WorkersDTO(WorkersAddDTO):
    id: int

class ResumesAddDTO(BaseModel):
    title: str
    compensation: int
    workload: Workload
    worker_id: int

class ResumesDTO(ResumesAddDTO):
    id: int
    created_at: datetime
    updated_at: datetime

class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"

class WorkersRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]

class WorkloadAvgCompensationDTO(BaseModel):
    workload: Workload
    avg_compensation: int
# DTO - Data Transfer Object(Просто передача данных)

class VacanciesAddDTO(BaseModel):
    title: str
    compensation: int | None

class VacanciesDTO(VacanciesAddDTO):
    id: int

class ResumesRelVacanciesReokiedDTO(ResumesDTO):
    worker: "WorkersDTO"
    vacancies_replied: list["VacanciesDTO"]