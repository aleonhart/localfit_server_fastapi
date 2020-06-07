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
    treadmill = "treadmill"
    stairmaster = "stairmaster"
    beat_saber = "beat_saber"
    cardio = "cardio"
    elliptical = "elliptical"


class ActivityFile(BaseModel):
    filename: str
    activity_type: ActivityTypeEnum
    is_manually_entered: bool
    activity_collection: str
    start_time_utc: datetime

    class Config:
        orm_mode = True


class ActivitySession(BaseModel):
    start_time_utc: datetime

    class Config:
        orm_mode = True
