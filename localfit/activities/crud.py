# stdlib
from typing import List

# 3rd Party
from sqlalchemy.orm import Session

# local
from localfit.activities import models
from localfit import schemas
from localfit.utilities import get_date_obj_from_string


def create_activity(db: Session, activity_file: schemas.ActivityFile, activity_records=List[schemas.ActivityRecord]):
    activity_file_obj = models.ActivityFile(**activity_file.dict())
    db.add(activity_file_obj)
    db.flush()  # get the id for the file object pre-save

    activity_records_objs = []
    for activity_record in activity_records:
        activity_record.update(file_id=activity_file_obj.id)
        activity_record_obj = models.ActivityRecord(**activity_record)
        activity_records_objs.append(activity_record_obj)

    db.bulk_save_objects(activity_records_objs)
    db.commit()
    db.refresh(activity_file_obj)
    return activity_file_obj


def update_activity(db: Session, filename: str, activity_file: schemas.ActivityFilePatch):
    activity_file_obj = db.query(models.ActivityFile).filter_by(filename=filename).one()
    for key, value in activity_file.dict().items():
        setattr(activity_file_obj, key, value)
    db.add(activity_file_obj)
    db.commit()
    return activity_file_obj


def delete_activity(db: Session, filename: str):
    activity_file_obj = db.query(models.ActivityFile).filter_by(filename=filename).one()
    db.delete(activity_file_obj)
    db.commit()


def get_activities_recent(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ActivityFile).order_by(models.ActivityFile.start_time_utc.desc()).offset(skip).limit(limit).all()


def get_activities_top(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ActivityFile).order_by(models.ActivityFile.total_distance.desc()).offset(skip).limit(limit).all()


def get_activities_calendar(year, db: Session, skip: int = 0, limit: int = 1000):
    start_date_obj = get_date_obj_from_string(f"{year}-01-01")
    end_date_obj = get_date_obj_from_string(f"{year}-12-31")

    return db.query(models.ActivityFile
                    ).filter(models.ActivityFile.start_time_utc >= start_date_obj,
                      models.ActivityFile.start_time_utc <= end_date_obj
                    ).order_by(models.ActivityFile.start_time_utc.asc()
                    ).offset(skip).limit(limit).all()


def get_activity_maps_by_collection(db: Session, collection_name: schemas.ActivityCollectionEnum,
                                 skip: int = 0, limit: int = 1000):

    maps = []
    files = db.query(models.ActivityFile).filter_by(activity_collection=collection_name).offset(skip).limit(limit).all()

    for file in files:
        records = [
            {
                "lat": record.position_lat_deg,
                "lng": record.position_long_deg
            } for record in db.query(models.ActivityRecord
                                     ).filter(models.ActivityRecord.file_id == file.id,
                                              models.ActivityRecord.position_lat_deg.isnot(None),
                                              models.ActivityRecord.position_long_deg.isnot(None)
                                              ).all()
        ]
        maps.append(records)
    return maps


def get_activity_by_filename(db: Session, filename: str):
    return db.query(models.ActivityFile).filter_by(filename=filename).one()


def get_activity_gps_records_by_filename(db: Session, filename: str):
    return [
        {
            "lat": r.position_lat_deg,
            "lng": r.position_long_deg
        } for r in db.query(models.ActivityRecord
                            ).join(models.ActivityFile
                            ).filter(models.ActivityFile.filename == filename,
                                     models.ActivityRecord.position_lat_deg.isnot(None),
                                     models.ActivityRecord.position_long_deg.isnot(None)
                                     ).all()
    ]


def get_activity_heart_rate_by_filename(db: Session, filename: str):
    return db.query(models.ActivityRecord
                    ).join(models.ActivityFile
                    ).filter(models.ActivityFile.filename == filename,
                             models.ActivityRecord.heart_rate.isnot(None),
                             ).order_by(models.ActivityRecord.timestamp_utc.desc()
                                        ).all()
