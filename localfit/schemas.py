# Pydantic models

# stdlib
from datetime import datetime
from decimal import Decimal
from enum import Enum

# 3rd Party
from pydantic import BaseModel
from typing import Optional, Any


class ActivityTypeEnum(str, Enum):
    yoga = "yoga"
    walk = "walk"
    cycling = "cycling"
    indoor_walk = "indoor_walk"
    run = "run"
    treadmill = "treadmill"
    stairmaster = "stairmaster"
    beat_saber = "beat_saber"
    cardio = "cardio"
    elliptical = "elliptical"
    stair = "stair"


class ActivityCollectionEnum(str, Enum):
    la_hikes = "la_hikes"
    neighborhood_runs = "neighborhood_runs"
    la_road_runners = "la_road_runners"
    oregon_hikes = "oregon_hikes"
    ali_walks_cc = "ali_walks_cc"
    ali_walks_sm = "ali_walks_sm"


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


class ActivityFilePatch(BaseModel):
    activity_collection: Optional[ActivityCollectionEnum]
    activity_type: Optional[ActivityTypeEnum]

    class Config:
        orm_mode = True


class ActivityListDisplay(BaseModel):
    """
    Some values change type when converted for display.
    This schema represents the display types.

    Eg. A Decimal timespan saved in the database is displayed as a string.
    """
    filename: str
    activity_type: ActivityTypeEnum
    is_manually_entered: bool
    activity_collection: str
    start_time_utc: str
    total_elapsed_time: str
    total_timer_time: Decimal
    total_distance: Optional[Decimal]
    total_calories: Optional[int]
    start_location: Optional[str]

    class Config:
        orm_mode = True


class ActivityRecord(BaseModel):
    file_id: int
    timestamp_utc: datetime
    heart_rate: Optional[int]
    position_lat_sem: Optional[int]
    position_long_sem: Optional[int]
    position_lat_deg: Optional[Decimal]
    position_long_deg: Optional[Decimal]
    distance: Optional[Decimal]
    altitude: Optional[Decimal]
    speed: Optional[int]
    cadence: Optional[int]
    fractional_cadence: Optional[Decimal]
    enhanced_altitude: Optional[Decimal]
    enhanced_speed: Optional[Decimal]

