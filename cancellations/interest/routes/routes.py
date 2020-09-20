# stdlib
from datetime import datetime
from typing import List

# 3rd Party
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

# local
from cancellations.db.database import get_db
from cancellations import schemas
from cancellations.interest.formatters.retrieval import get_formatted_points_of_interest


router = APIRouter()


@router.get("/points/", response_model=List[schemas.InterestPointResponse])
def get_cancellations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_formatted_points_of_interest(db, skip=skip, limit=limit)
