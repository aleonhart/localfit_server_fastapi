# 3rd Party
from datetime import datetime
from fastapi import Depends, File, UploadFile
from fastapi import APIRouter
from fitparse import FitFile
from typing import List
from sqlalchemy.orm import Session

# local
from localfit.db import crud
from localfit.db.database import get_db
from localfit import schemas


router = APIRouter()


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
    activity_file_data = {
        "filename": file.filename.split(".")[0],
        "activity_type": serializer,

    }
    activity_file = schemas.ActivityFile(**activity_file_data)

    activity_session_data = {
        "start_time_utc": datetime.utcnow(),
    }
    activity_session = schemas.ActivitySession(**activity_session_data)
    return crud.create_activity(session=db, activity_file=activity_file, activity_session=activity_session)
