# 3rd Party
from fastapi import Depends, File, UploadFile
from fastapi import APIRouter
from sqlalchemy.orm import Session

# local
from localfit.db import crud
from localfit.db.database import get_db
from localfit import schemas
from localfit.activities.fileupload import get_activity_data


router = APIRouter()


@router.post("/uploadfile/", response_model=schemas.ActivityFile)
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    activity_file, activity_session = get_activity_data(file)
    return crud.create_activity(session=db, activity_file=activity_file, activity_session=activity_session)
