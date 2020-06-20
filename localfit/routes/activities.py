# stdlib
from typing import List

# 3rd Party
from fastapi import Depends, File, UploadFile, Path
from fastapi import APIRouter
from fitparse import FitFile
from sqlalchemy.orm import Session

# local
from localfit.db import crud
from localfit.db.database import get_db
from localfit import schemas
from localfit.activities.formatters.upload import get_activity_data, get_activity_record_data
from localfit.activities.formatters.retrieval import get_activity_metadata_by_filename


router = APIRouter()


@router.post("/activities/", response_model=schemas.ActivityFile)
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    fit_file = FitFile(file.file)
    activity_file = get_activity_data(file, fit_file)
    activity_records = get_activity_record_data(fit_file)
    return crud.create_activity(session=db, activity_file=activity_file, activity_records=activity_records)


@router.get("/activities/", response_model=List[schemas.ActivityFile])
def get_activities_recent(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_activities_recent(db, skip=skip, limit=limit)
    return items


@router.get("/activities/{filename}/")
async def read_items(filename: str = Path(..., title="The filename of a single activity"), db: Session = Depends(get_db)):
    return get_activity_metadata_by_filename(db, filename)


@router.get("/activities/top/", response_model=List[schemas.ActivityFile])
def get_activities_top(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_activities_top(db, skip=skip, limit=limit)
    return items
