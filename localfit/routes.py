# 3rd Party
from datetime import datetime
from fastapi import Depends, File, UploadFile
from fastapi import APIRouter
from fitparse import FitFile
import pytz
from sqlalchemy.orm import Session

# local
from localfit.db import crud
from localfit.db.database import get_db
from localfit import schemas


router = APIRouter()


def _get_activity_session_data(fit_file):
    session_data = [row for row in fit_file.get_messages('session')][0]
    formatted_session_data = {
        'start_time_utc': pytz.utc.localize(session_data.get('start_time').value),
        'total_elapsed_time': session_data.get('total_elapsed_time').value,
        'total_timer_time': session_data.get('total_timer_time').value,
        'total_distance': session_data.get('total_distance').value,
        'total_strides': session_data.get('total_strides').value if session_data.get('total_strides') else None,
        'total_cycles': session_data.get('total_cycles').value if session_data.get('total_cycles') else None,
        'total_calories': session_data.get('total_calories').value,
        'enhanced_avg_speed': session_data.get('enhanced_avg_speed').value,
        'avg_speed': session_data.get('avg_speed').value,
        'enhanced_max_speed': session_data.get('enhanced_max_speed').value,
        'max_speed': session_data.get('max_speed').value,
        'avg_power': session_data.get('avg_power').value,
        'max_power': session_data.get('max_power').value,
        'total_ascent': session_data.get('total_ascent').value,
        'total_descent': session_data.get('total_descent').value,
    }
    return formatted_session_data


SPORT_TO_SERIALIZER = {
    (1, 0): "run",              # Run: generic
    (1, 1): "treadmill",        # Run: Treadmill
    (4, 15): "elliptical",      # Fitness Equipment: Elliptical
    (11, 0): "walk",            # walk
    (10, 43): "yoga",           # yoga
    (4, 16): "stair",   # Fitness Equipment: Stair Climbing
    (10, 26): "cardio",  # Training: Cardio (Beat Saber)
}


def _get_serializer_by_sport(fit_file):
    sport_data = [r for r in fit_file.get_messages('sport') if r.type == 'data'][0]
    try:
        serializer = SPORT_TO_SERIALIZER[(sport_data.get("sport").raw_value, sport_data.get("sub_sport").raw_value)]
    except KeyError:
        raise Exception({"file": "Unsupported sport"})
    return serializer


@router.post("/uploadfile/", response_model=schemas.ActivityFile)
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    fit_file = FitFile(file.file)
    serializer = _get_serializer_by_sport(fit_file)

    activity_session_data = _get_activity_session_data(fit_file)
    activity_session = schemas.ActivitySession(**activity_session_data)

    activity_file_data = {
        "filename": file.filename.split(".")[0],
        "activity_type": serializer,
        "is_manually_entered": False,
        "activity_collection": "uncategorized",
        "start_time_utc": activity_session.start_time_utc,

    }
    activity_file = schemas.ActivityFile(**activity_file_data)

    return crud.create_activity(session=db, activity_file=activity_file, activity_session=activity_session)
