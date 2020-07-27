# SQLAlchemy models

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from localfit.db.database import Base


class MonitorFile(Base):
    """
    MONITOR files
    """

    __tablename__ = "monitor_file"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)

    """
    RELATIONSHIPS

    backref: 
        establishes relationship: MonitorFile.<name>_records 
        establishes relationship: <Name>Data.monitor_file

    cascade:
        save-update: Default behavior. Indicates that when an object is placed into a Session via Session.add(), all 
            the objects associated with it via this relationship() should also be added to that same Session.
        merge: Default behavior. Indicates that the Session.merge() operation should be propagated from a parent that’s 
            the subject of the Session.merge() call down to referred objects. 
        delete: Indicates that when a “parent” object is marked for deletion, its related “child” objects should also 
            be marked for deletion.
    """
    heart_rate_records = relationship("HeartRateData", backref="monitor_file", cascade="save-update, merge, delete")
    metabolic_rate_records = relationship("MetabolicRateData", backref="monitor_file", cascade="save-update, merge, delete")
    stress_records = relationship("StressData", backref="monitor_file", cascade="save-update, merge, delete")
    step_records = relationship("StepData", backref="monitor_file", cascade="save-update, merge, delete")


class HeartRateData(Base):
    """
    Heart rate data from MONITOR files
    """

    __tablename__ = "monitor_heart_rate"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    heart_rate = Column(Integer)


class MetabolicRateData(Base):
    """
    Resting metabolic rate data from MONITOR files
    """

    __tablename__ = "monitor_meta_rate"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    resting_metabolic_rate = Column(Integer)  # KCAL


class StepData(Base):
    """
    Daily step data from MONITOR files
    """

    __tablename__ = "monitor_step"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    steps = Column(Integer)


class StressData(Base):
    """
    Stress data from MONITOR files
    """

    __tablename__ = "monitor_stress"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    stress_level = Column(Integer)
