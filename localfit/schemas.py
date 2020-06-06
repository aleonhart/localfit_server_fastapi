# Pydantic models

from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ActivityTypeEnum(str, Enum):
    yoga = "yoga"
    walk = "walk"
    run = "run"


class ActivityFile(BaseModel):
    filename: str
    activity_type: ActivityTypeEnum

    class Config:
        orm_mode = True


class ActivitySession(BaseModel):
    start_time_utc: datetime

    class Config:
        orm_mode = True
