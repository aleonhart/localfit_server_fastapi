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


def create_activity(db: Session, activity: schemas.Activity):  # does this need to be ActivityCreate ?
    db_item = models.ActivityFile(**activity)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
