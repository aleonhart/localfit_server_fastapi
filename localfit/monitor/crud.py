# stdlib
from datetime import date
from typing import List

# 3rd Party
from sqlalchemy.orm import Session

# local
from localfit.monitor import models
from localfit.monitor import schemas


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
                        heart_rate_data=List[schemas.HeartRateData],
                        metabolic_rate_data=List[schemas.MetabolicRateData],
                        #step_data=schemas.StepData,
                        stress_data=List[schemas.StressData]):

    monitor_file_obj = models.MonitorFile(**monitor_file.dict())
    db.add(monitor_file_obj)
    db.flush()  # get the id for the file object pre-save

    heart_rate_objs = []
    for heart_rate in heart_rate_data:
        heart_rate.update(file_id=monitor_file_obj.id)
        heart_rate_objs.append(models.HeartRateData(**heart_rate))

    db.bulk_save_objects(heart_rate_objs)

    metabolic_rate_objs = []
    for meta_rate in metabolic_rate_data:
        meta_rate.update(file_id=monitor_file_obj.id)
        metabolic_rate_objs.append(models.MetabolicRateData(**meta_rate))

    db.bulk_save_objects(metabolic_rate_objs)

    """
    TODO step data
    step_data_obj = crud.get_step_data_by_date(db, local_date)

    # only bother to update the data if it doesn't exist or is less than the value we found now
    if not step_data_obj:
        schemas.StepData(filename=file.filename.split(".")[0])
        crud.create_step_data_for_date(db, local_date, record['steps'])
    elif step_data_obj.steps < record['steps']:
        crud.update_step_data_for_date(db, local_date, record['steps'])
        
    """

    stress_objs = []
    for stress in stress_data:
        stress.update(file_id=monitor_file_obj.id)
        stress_objs.append(models.StressData(**stress))

    db.bulk_save_objects(stress_objs)

    db.commit()
    db.refresh(monitor_file_obj)
    return monitor_file_obj
