from sqlalchemy.orm import Session

from . import models
from localfit import schemas


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_activity(session: Session, activity_file: schemas.ActivityFile, activity_session: schemas.ActivitySession):
    activity_file_obj = models.ActivityFile(**activity_file.dict())
    session.add(activity_file_obj)
    session.commit()
    session.refresh(activity_file_obj)

    activity_session_obj = models.ActivitySession(**activity_session.dict(), file_id=activity_file_obj.id)
    session.add(activity_session_obj)
    session.commit()
    session.refresh(activity_session_obj)

    return activity_file_obj
