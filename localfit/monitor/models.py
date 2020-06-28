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

    # relationships
    monitor_heart_rate = relationship("HeartRateData", back_populates="file")
    monitor_meta_rate = relationship("MetabolicRateData", back_populates="file")
    monitor_step = relationship("StepData", back_populates="file")
    monitor_stress = relationship("StressData", back_populates="file")


class HeartRateData(Base):
    """
    Heart rate data from MONITOR files
    """

    __tablename__ = "monitor_heart_rate"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    heart_rate = Column(Integer)

    # relationships
    file = relationship("MonitorFile", back_populates="monitor_heart_rate")


class MetabolicRateData(Base):
    """
    Resting metabolic rate data from MONITOR files
    """

    __tablename__ = "monitor_meta_rate"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    timestamp_utc = Column(DateTime, nullable=False, unique=True)
    resting_metabolic_rate = Column(Integer)  # KCAL

    # relationships
    file = relationship("MonitorFile", back_populates="monitor_meta_rate")


class StepData(Base):
    """
    Daily step data from MONITOR files
    """

    __tablename__ = "monitor_step"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    step_date = Column(Date, nullable=False, unique=True)
    steps = Column(Integer)

    # relationships
    file = relationship("MonitorFile", back_populates="monitor_step")


class StressData(Base):
    """
    Stress data from MONITOR files
    """

    __tablename__ = "monitor_stress"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("monitor_file.id"))
    stress_level_time_utc = Column(DateTime, nullable=False, unique=True)
    stress_level_value = Column(Integer)

    # relationships
    file = relationship("MonitorFile", back_populates="monitor_stress")
