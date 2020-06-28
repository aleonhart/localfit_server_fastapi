# stdlib

# 3rd Party
from fastapi import Depends, File, UploadFile, Path
from fastapi import APIRouter
from fitparse import FitFile
from sqlalchemy.orm import Session

# local
from localfit.activities import crud
from localfit.db.database import get_db
from localfit import schemas
from localfit.activities.formatters.upload import get_activity_data, get_activity_record_data, update_activity_metadata
from localfit.activities.formatters.retrieval import get_activity_metadata_by_filename, get_activity_map_by_filename


activity_router = APIRouter()

"""
Functions supporting singular operations on the /activities/ API
"""


@activity_router.post("/activities/", response_model=schemas.ActivityFile)
async def upload_activity_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    fit_file = FitFile(file.file)
    activity_file = get_activity_data(file, fit_file)
    activity_records = get_activity_record_data(fit_file)
    return crud.create_activity(db=db, activity_file=activity_file, activity_records=activity_records)


@activity_router.patch("/activities/{filename}/")
async def update_activity(activity_file: schemas.ActivityFilePatch,
                           filename: str = Path(..., title="The filename of a single activity"),
                           db: Session = Depends(get_db)):
    return update_activity_metadata(db, filename, activity_file)


@activity_router.get("/activities/{filename}/")
async def get_activity_metadata(filename: str = Path(..., title="The filename of a single activity"),
                                db: Session = Depends(get_db)):
    return get_activity_metadata_by_filename(db, filename)


@activity_router.get("/activities/{filename}/map/")
async def get_activity_map(filename: str = Path(..., title="The filename of a single activity"),
                           db: Session = Depends(get_db)):
    return get_activity_map_by_filename(db, filename)
