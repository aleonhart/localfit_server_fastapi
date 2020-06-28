# stdlib
from datetime import date
from typing import List

# 3rd Party
from sqlalchemy.orm import Session

# local
from localfit.monitor import models
from localfit.monitor import schemas
from localfit.utilities import localize_datetime_for_display, get_date_obj_from_string


def get_step_data_by_date(db: Session, step_date: date):
    steps = db.query(models.StepData).filter_by(step_date=step_date)
    return steps.one() if steps.scalar() else None


def create_step_data_for_date(db: Session, step_data: schemas.StepData):
    step_obj = models.MonitorFile(**step_data.dict())
    db.add(step_obj)
    db.commit()
    db.refresh(step_obj)
    return step_obj


def update_step_data_for_date(db: Session, step_date: date, steps: int):
    step_data_obj = db.query(models.StepData).filter_by(step_date=step_date).one()
    setattr(step_data_obj, "step_date", step_date)
    db.add(step_data_obj)
    db.commit()
    return step_data_obj


def create_monitor_data(db: Session,
                        monitor_file=schemas.MonitorFile,
                        heart_rate_data_list=List[schemas.HeartRateData],
                        metabolic_rate_data_list=List[schemas.MetabolicRateData],
                        step_data=schemas.StepData,
                        stress_data_list=List[schemas.StressData]):

    monitor_file_obj = models.MonitorFile(**monitor_file.dict())
    db.add(monitor_file_obj)
    db.flush()  # get the id for the file object pre-save

    heart_rate_objs = []
    for heart_rate in heart_rate_data_list:
        heart_rate.update(file_id=monitor_file_obj.id)
        heart_rate_objs.append(models.HeartRateData(**heart_rate))

    db.bulk_save_objects(heart_rate_objs)

    metabolic_rate_objs = []
    for meta_rate in metabolic_rate_data_list:
        meta_rate.update(file_id=monitor_file_obj.id)
        metabolic_rate_objs.append(models.MetabolicRateData(**meta_rate))

    db.bulk_save_objects(metabolic_rate_objs)

    # This is needed because ANT files are written from local time start to stop.
    # This ensures you grab the correct file for your device's timezone.
    #
    # For example
    # If your device is UTC+1, your file will write a "day" from 1:00 AM - 12:59 AM
    # If your device is UTC+8, your file will write a "day" from 8:00 AM - 7:59 AM
    local_date = localize_datetime_for_display(step_data['step_date']).date()

    steps_query = db.query(models.StepData).filter_by(step_date=local_date)

    # only bother to update the data if it doesn't exist or is less than the value we found now
    if not steps_query.scalar():
        step = schemas.StepData(file_id=monitor_file_obj.id, steps=step_data['steps'], step_date=step_data['step_date'])
        steps_obj = models.StepData(**step.dict())
        db.add(steps_obj)
    else:
        steps_obj = steps_query.one()
        if steps_obj.steps < step_data['steps']:
            steps_obj.steps = step_data['steps']
            db.add(steps_obj)

    stress_objs = []
    for stress in stress_data_list:
        stress.update(file_id=monitor_file_obj.id)
        stress_objs.append(models.StressData(**stress))

    db.bulk_save_objects(stress_objs)

    db.commit()
    db.refresh(monitor_file_obj)
    return monitor_file_obj


def get_monitor_steps_by_date(start_date, end_date, db: Session):
    return db.query(models.StepData
                    ).filter(models.StepData.step_date >= start_date, models.StepData.step_date <= end_date
                    ).order_by(models.StepData.step_date.asc()
                    ).offset(0).limit(366).all()


def get_monitor_step_goal(year, month, days_in_month, db: Session):
    start_date_obj = get_date_obj_from_string(f"{year}-{month}-01")
    end_date_obj = get_date_obj_from_string(f"{year}-{month}-{days_in_month}")

    return db.query(models.StepData
             ).filter(models.StepData.step_date >= start_date_obj,
                      models.StepData.step_date <= end_date_obj
             ).order_by(models.StepData.step_date.asc()
             ).offset(0).limit(31).all()
