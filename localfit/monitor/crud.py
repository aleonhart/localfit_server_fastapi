# stdlib
from datetime import datetime, timedelta
from typing import List

# 3rd Party
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

# local
from localfit.monitor import models
from localfit.monitor import schemas
from localfit.utilities import localize_datetime_for_display, get_date_obj_from_string


def get_step_data_by_date(db: Session, timestamp_utc: datetime):
    steps = db.query(models.StepData).filter_by(timestamp_utc=timestamp_utc)
    return steps.one() if steps.scalar() else None


def create_step_data_for_date(db: Session, step_data: schemas.StepData):
    step_obj = models.MonitorFile(**step_data.dict())
    db.add(step_obj)
    db.commit()
    db.refresh(step_obj)
    return step_obj


def update_step_data_for_date(db: Session, timestamp_utc: datetime, steps: int):
    step_data_obj = db.query(models.StepData).filter_by(timestamp_utc=timestamp_utc).one()
    setattr(step_data_obj, "timestamp_utc", timestamp_utc)
    db.add(step_data_obj)
    db.commit()
    return step_data_obj


def _handle_heart_rate_data(db, monitor_file_obj, heart_rate_data_list):
    heart_rate_objs = []
    for heart_rate in heart_rate_data_list:
        heart_rate.update(file_id=monitor_file_obj.id)
        heart_rate_objs.append(models.HeartRateData(**heart_rate))
    db.bulk_save_objects(heart_rate_objs)


def _handle_metabolic_rate_data(db, monitor_file_obj, metabolic_rate_data_list):
    metabolic_rate_objs = []
    for meta_rate in metabolic_rate_data_list:
        meta_rate.update(file_id=monitor_file_obj.id)
        metabolic_rate_objs.append(models.MetabolicRateData(**meta_rate))
    db.bulk_save_objects(metabolic_rate_objs)


def _handle_step_data(db, monitor_file_obj, step_data):
    step_date_start = step_data['timestamp_utc']
    step_date_start = step_date_start.replace(hour=0, minute=0, second=0)
    step_date_end = step_date_start + timedelta(days=1)

    try:
        step_obj = db.query(models.StepData).filter(models.StepData.timestamp_utc >= step_date_start,
                                     models.StepData.timestamp_utc < step_date_end).one()

        if step_data['steps'] > step_obj.steps:
            step_obj.steps = step_data['steps']
            db.add(step_obj)
    except NoResultFound as e:
        step_data.update(file_id=monitor_file_obj.id)
        step_obj = models.StepData(**step_data)
        db.add(step_obj)


def _handle_stress_data(db, monitor_file_obj, stress_data_list):
    stress_objs = []
    for stress in stress_data_list:
        stress.update(file_id=monitor_file_obj.id)
        stress_objs.append(models.StressData(**stress))
    db.bulk_save_objects(stress_objs)


def create_monitor_data(db: Session,
                        monitor_file=schemas.MonitorFile,
                        heart_rate_data_list=List[schemas.HeartRateData],
                        metabolic_rate_data_list=List[schemas.MetabolicRateData],
                        step_data=schemas.StepData,
                        stress_data_list=List[schemas.StressData]):

    monitor_file_obj = models.MonitorFile(**monitor_file.dict())
    db.add(monitor_file_obj)
    db.flush()  # get the id for the monitor file object pre-save

    _handle_heart_rate_data(db, monitor_file_obj, heart_rate_data_list)
    _handle_metabolic_rate_data(db, monitor_file_obj, metabolic_rate_data_list)
    _handle_step_data(db, monitor_file_obj, step_data)
    _handle_stress_data(db, monitor_file_obj, stress_data_list)

    db.commit()
    db.refresh(monitor_file_obj)
    return monitor_file_obj


def get_monitor_steps_by_date(start_date, end_date, db: Session):
    return db.query(models.StepData
                    ).filter(models.StepData.timestamp_utc >= start_date, models.StepData.timestamp_utc < end_date
                    ).order_by(models.StepData.timestamp_utc.asc()
                    ).offset(0).limit(366).all()


def get_monitor_step_goal(year, month, days_in_month, db: Session):
    start_date_obj = get_date_obj_from_string(f"{year}-{month}-01")
    end_date_obj = get_date_obj_from_string(f"{year}-{month}-{days_in_month}")

    return db.query(models.StepData
             ).filter(models.StepData.timestamp_utc >= start_date_obj,
                      models.StepData.timestamp_utc <= end_date_obj
             ).order_by(models.StepData.timestamp_utc.asc()
             ).offset(0).limit(31).all()
