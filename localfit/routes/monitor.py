# stdlib

# 3rd Party
from fastapi import Depends, File, UploadFile
from fastapi import APIRouter
from fitparse import FitFile
from sqlalchemy.orm import Session

# local
from localfit.monitor import crud
from localfit.db.database import get_db
from localfit.monitor import schemas
from localfit.monitor.formatters import upload


monitor_router = APIRouter()

"""
Functions supporting singular operations on the /monitor/ API
"""


@monitor_router.post("/monitors/", response_model=schemas.MonitorFile)
async def upload_monitor_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    fit_file = FitFile(file.file)
    monitor_file = schemas.MonitorFile(filename=file.filename.split(".")[0])

    heart_rate_data = upload.parse_heart_rate_data_from_monitor_file(fit_file)
    metabolic_rate_data = upload.parse_heart_metabolic_rate_from_monitor_file(fit_file)
    #step_data = upload.parse_step_data_from_monitor_file(db, fit_file)
    stress_data = upload.parse_stress_data_from_monitor_file(fit_file)

    return crud.create_monitor_data(db=db,
                                    monitor_file=monitor_file,
                                    heart_rate_data=heart_rate_data,
                                    metabolic_rate_data=metabolic_rate_data,
                                    #step_data=step_data,
                                    stress_data=stress_data)
