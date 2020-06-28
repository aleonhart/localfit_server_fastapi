# stdlib
from typing import List

# 3rd Party
from sqlalchemy.orm import Session

# local
from localfit.activities.models import ActivityFile, ActivityRecord
from localfit import schemas


def create_activity(db: Session, activity_file: schemas.ActivityFile, activity_records=List[schemas.ActivityRecord]):
    activity_file_obj = ActivityFile(**activity_file.dict())
    db.add(activity_file_obj)
    db.flush()  # get the id for the file object pre-save

    activity_records_objs = []
    for activity_record in activity_records:
        activity_record.update(file_id=activity_file_obj.id)
        activity_record_obj = ActivityRecord(**activity_record)
        activity_records_objs.append(activity_record_obj)

    db.bulk_save_objects(activity_records_objs)
    db.commit()
    db.refresh(activity_file_obj)
    return activity_file_obj


def update_activity(db: Session, filename: str, activity_file: schemas.ActivityFilePatch):
    activity_file_obj = db.query(ActivityFile).filter_by(filename=filename).one()
    for key, value in activity_file.dict().items():
        setattr(activity_file_obj, key, value)
    db.add(activity_file_obj)
    db.commit()
    return activity_file_obj


def get_activities_recent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ActivityFile).order_by(ActivityFile.start_time_utc.desc()).offset(skip).limit(limit).all()


def get_activity_by_filename(db: Session, filename: str):
    return db.query(ActivityFile).filter_by(filename=filename).one()


def get_activity_records_by_filename(db: Session, filename: str):
    return [
        {
            "lat": r.position_lat_deg,
            "lng": r.position_long_deg
        } for r in db.query(ActivityRecord).join(ActivityFile).filter(ActivityFile.filename == filename).all()
    ]


def get_activities_top(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ActivityFile).order_by(ActivityFile.total_distance.desc()).offset(skip).limit(limit).all()


def get_activity_maps_by_collection(db: Session, collection_name: schemas.ActivityCollectionEnum,
                                 skip: int = 0, limit: int = 1000):

    maps = []
    files = db.query(ActivityFile).filter_by(activity_collection=collection_name).offset(skip).limit(limit).all()

    for file in files:
        records = [
            {
                "lat": record.position_lat_deg,
                "lng": record.position_long_deg
            } for record in db.query(ActivityRecord).filter(ActivityRecord.file == file).all()
        ]
        maps.append(records)
    return maps
