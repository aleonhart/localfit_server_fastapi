# stdlib
from datetime import datetime
from typing import List

# 3rd Party
from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import Session

# local
from localfit.activities import crud
from localfit.db.database import get_db
from localfit import schemas
from localfit.activities.formatters.retrieval import (format_activity_maps_by_collection, get_formatted_top_activities,
                                                      format_activities_calendar)


activities_router = APIRouter()


"""
Functions supporting bulk operations on the /activities/ API
"""


@activities_router.get("/activities/", response_model=List[schemas.ActivityFile])
def get_activities_recent(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_activities_recent(db, skip=skip, limit=limit)


@activities_router.get("/activities/top/", response_model=List[schemas.ActivityListDisplay])
def get_activities_top(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_formatted_top_activities(db, skip=skip, limit=limit)


@activities_router.get("/activities/calendar/")
def get_activities_calendar(year: str = None, skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    now = datetime.now()
    year = year or str(now.year)
    return format_activities_calendar(year, db, skip, limit)


@activities_router.get("/activities/collection/{collection_name}/")
def get_activity_collection(collection_name: str = Path(..., title="The name of the collection of activities"),
                            skip: int = 0,
                            limit: int = 1000,
                            db: Session = Depends(get_db)):
    return format_activity_maps_by_collection(db, collection_name=collection_name, skip=skip, limit=limit)
