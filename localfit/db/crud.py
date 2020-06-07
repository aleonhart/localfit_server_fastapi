from sqlalchemy.orm import Session

from localfit.db.models import ActivityFile
from localfit import schemas


def create_activity(session: Session, activity_file: schemas.ActivityFile):
    activity_file_obj = ActivityFile(**activity_file.dict())
    session.add(activity_file_obj)
    session.commit()
    session.refresh(activity_file_obj)

    return activity_file_obj


def get_activities_recent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActivityFile).order_by(ActivityFile.start_time_utc.desc()).offset(skip).limit(limit).all()


def get_activities_top(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ActivityFile).order_by(ActivityFile.total_distance.desc()).offset(skip).limit(limit).all()
