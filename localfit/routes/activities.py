# stdlib
from typing import List

# 3rd Party
from fastapi import Depends
from fastapi import APIRouter
from sqlalchemy.orm import Session

# local
from localfit.db import crud
from localfit.db.database import get_db
from localfit import schemas


activities_router = APIRouter()


"""
Functions supporting bulk operations on the /activities/ API
"""


@activities_router.get("/activities/", response_model=List[schemas.ActivityFile])
def get_activities_recent(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_activities_recent(db, skip=skip, limit=limit)
    return items


@activities_router.get("/activities/top/", response_model=List[schemas.ActivityFile])
def get_activities_top(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = crud.get_activities_top(db, skip=skip, limit=limit)
    return items
