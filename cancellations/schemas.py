# Pydantic models

# stdlib
from datetime import datetime
from decimal import Decimal

# 3rd Party
from pydantic import BaseModel


class Abbreviation(BaseModel):
    abbrev: str
    name: str

    class Config:
        orm_mode = True


class InterestPointMetaData(BaseModel):
    name: str
    abbrev: str
    location_name: str
    state: str

    class Config:
        orm_mode = True


class InterestPointResponse(BaseModel):
    meta: InterestPointMetaData
    lat_deg: Decimal
    long_deg: Decimal

    class Config:
        orm_mode = True
