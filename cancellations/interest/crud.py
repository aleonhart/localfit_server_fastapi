# stdlib
from typing import List

# 3rd Party
from sqlalchemy.orm import Session

# local
from cancellations.interest import models


def get_points_of_interest(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InterestPoint).order_by(models.InterestPoint.state.asc()).offset(skip).limit(limit).all()

