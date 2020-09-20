# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from cancellations.db.database import Base


class Abbreviation(Base):
    __tablename__ = "abbreviation"

    abbrev_id = Column(Integer, primary_key=True)
    abbrev = Column(String, unique=True, nullable=False)
    name = Column(String)


class InterestPoint(Base):
    __tablename__ = "interest_point"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    abbrev = Column(Integer, ForeignKey("abbreviation.abbrev"))
    location_name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    lat_deg = Column(Numeric(precision=8, scale=6), nullable=False)    #      XX.XXXXXX degrees
    long_deg = Column(Numeric(precision=9, scale=6), nullable=False)   #     XXX.XXXXXX degrees
    """
    RELATIONSHIPS

    backref: 
        establishes relationship: InterestPoint.abbrev 
        establishes relationship: Abbreviation.interest_point

    cascade:
        save-update: Default behavior. Indicates that when an object is placed into a Session via Session.add(), all 
            the objects associated with it via this relationship() should also be added to that same Session.
        merge: Default behavior. Indicates that the Session.merge() operation should be propagated from a parent that’s 
            the subject of the Session.merge() call down to referred objects. 
        delete: Indicates that when a “parent” object is marked for deletion, its related “child” objects should also 
            be marked for deletion.
    """
    # abbrev = relationship("Abbreviation", backref="interest_point", cascade="save-update, merge, delete")
