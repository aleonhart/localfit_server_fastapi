# stdlib
from typing import List
from calendar import monthrange
from datetime import datetime

# 3rd Party
from fastapi import Depends, File, UploadFile
from fastapi import APIRouter
from fitparse import FitFile
from sqlalchemy.orm import Session

# local
from localfit import utilities
from localfit.monitor import crud
from localfit.db.database import get_db
from localfit.monitor import schemas
from localfit.monitor.formatters import upload, steps

monitor_router = APIRouter()


@monitor_router.post("/monitor/", response_model=schemas.MonitorFile)
async def upload_monitor_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    fit_file = FitFile(file.file)
    monitor_file = schemas.MonitorFile(filename=file.filename.split(".")[0])

    heart_rate_data_list = upload.parse_heart_rate_data_from_monitor_file(fit_file)
    metabolic_rate_data_list = upload.parse_heart_metabolic_rate_from_monitor_file(fit_file)
    step_data = upload.parse_step_data_from_monitor_file(fit_file)
    stress_data_list = upload.parse_stress_data_from_monitor_file(fit_file)

    return crud.create_monitor_data(db=db,
                                    monitor_file=monitor_file,
                                    heart_rate_data_list=heart_rate_data_list,
                                    metabolic_rate_data_list=metabolic_rate_data_list,
                                    step_data=step_data,
                                    stress_data_list=stress_data_list)


@monitor_router.get("/monitor/steps/")
def get_steps_by_date(start_date, end_date, db: Session = Depends(get_db)):
    local_start_datetime = utilities.localize_datetime_for_display(
        utilities.localize_datetime_to_utc_for_storage(
            utilities.get_datetime_obj_from_string(start_date)))

    local_end_datetime = utilities.localize_datetime_for_display(
        utilities.localize_datetime_to_utc_for_storage(
            utilities.get_datetime_obj_from_string(end_date)))
    return steps.format_steps_for_display(local_start_datetime, local_end_datetime, db)


@monitor_router.get("/monitor/steps/goal/")
def get_step_goal_by_month(year: int = None, month: int = None, db: Session = Depends(get_db)):
    """

    data = StepData.objects.filter(date__gte=f"{now.year}-{now.month}-01", date__lte=f"{now.year}-{now.month}-{days_in_month}")
    serializer = StepGoalSerializer(data, context={'days_in_month': days_in_month}, many=True)
    return Response(serializer.data)

    """
    now = datetime.now()
    year = year or now.year
    month = month or now.month

    _, days_in_month = monthrange(year, month)
    return steps.get_percent_step_goal_achievement(year, month, days_in_month, db)

