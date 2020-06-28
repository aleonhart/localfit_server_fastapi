# Pydantic models

# stdlib
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

# 3rd Party
from pydantic import BaseModel
from typing import Optional


class MonitorFile(BaseModel):
    filename: str

    class Config:
        orm_mode = True


class HeartRateData(BaseModel):
    file_id: int
    timestamp_utc: datetime
    heart_rate: int

    class Config:
        orm_mode = True


class MetabolicRateData(BaseModel):
    file_id: int
    timestamp_utc: datetime
    resting_metabolic_rate: int

    class Config:
        orm_mode = True


class StepData(BaseModel):
    file_id: int
    step_date: date
    steps: int

    class Config:
        orm_mode = True


class StressData(BaseModel):
    file_id: int
    stress_level_time_utc: datetime
    stress_level_value: int

    class Config:
        orm_mode = True
