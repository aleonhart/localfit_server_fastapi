# Pydantic models

# stdlib
from datetime import datetime
from decimal import Decimal
from enum import Enum

# 3rd Party
from pydantic import BaseModel
from typing import Optional


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
    total_elapsed_time: Decimal
    total_timer_time: Decimal
    total_distance: Optional[Decimal]
    total_strides: Optional[int]
    total_cycles: Optional[int]
    total_calories: Optional[int]
    enhanced_avg_speed: Optional[Decimal]
    avg_speed: Optional[int]
    enhanced_max_speed: Optional[Decimal]
    max_speed: Optional[int]
    avg_power: Optional[int]
    max_power: Optional[int]
    total_ascent: Optional[int]
    total_descent: Optional[int]
    start_position_lat_sem: Optional[int]
    start_position_long_sem: Optional[int]
    start_position_lat_deg: Optional[Decimal]
    start_position_long_deg: Optional[Decimal]
    start_location: Optional[str]

    class Config:
        orm_mode = True
