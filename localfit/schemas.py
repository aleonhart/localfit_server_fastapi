# Pydantic models

# stdlib
from datetime import datetime
from decimal import Decimal
from enum import Enum

# 3rd Party
from pydantic import BaseModel


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
    total_elapsed_time: Decimal
    total_timer_time: Decimal
    total_distance: Decimal
    total_strides: int
    total_cycles = int
    total_calories = int
    enhanced_avg_speed = Decimal
    avg_speed = int
    enhanced_max_speed = Decimal
    max_speed = int
    avg_power = int
    max_power = int
    total_ascent = int
    total_descent = int

    class Config:
        orm_mode = True
