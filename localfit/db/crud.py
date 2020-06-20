# stdlib
from typing import List

# 3rd Party
from sqlalchemy.orm import Session, Query

# local
from localfit.db.models import ActivityFile, ActivityRecord
from localfit import schemas


def create_activity(session: Session, activity_file: schemas.ActivityFile, activity_records=List[schemas.ActivityRecord]):
    activity_file_obj = ActivityFile(**activity_file.dict())
    session.add(activity_file_obj)
    session.flush()  # get the id for the file object pre-save

    activity_records_objs = []
    for activity_record in activity_records:
        activity_record.update(file_id=activity_file_obj.id)
        activity_record_obj = ActivityRecord(**activity_record)
        activity_records_objs.append(activity_record_obj)

    session.bulk_save_objects(activity_records_objs)
    session.commit()
    session.refresh(activity_file_obj)
    return activity_file_obj


def get_activities_recent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActivityFile).order_by(ActivityFile.start_time_utc.desc()).offset(skip).limit(limit).all()


def get_activity_by_filename(db: Session, filename: str):
    return db.query(ActivityFile).filter_by(filename=filename).one()


def get_activities_top(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ActivityFile).order_by(ActivityFile.total_distance.desc()).offset(skip).limit(limit).all()
