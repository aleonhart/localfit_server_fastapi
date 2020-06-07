# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from localfit.db.database import Base


class ActivityFile(Base):
    __tablename__ = "activity_file"

    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    activity_type = Column(String, nullable=False)
    is_manually_entered = Column(Boolean, default=False)
    activity_collection = Column(String)
    start_time_utc = Column(DateTime, nullable=False)

    activity_session = relationship("ActivitySession", back_populates="file")


class ActivitySession(Base):
    __tablename__ = "activity_session"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("activity_file.id"))
    start_time_utc = Column(DateTime, nullable=False)
    total_elapsed_time = Column(Numeric(precision=10, scale=3))
    total_timer_time = Column(Numeric(precision=10, scale=3))
    total_distance = Column(Numeric(precision=8, scale=2))
    total_strides = Column(Integer)
    total_cycles = Column(Integer)
    total_calories = Column(Integer)
    enhanced_avg_speed = Column(Numeric(precision=5, scale=3))
    avg_speed = Column(Integer)
    enhanced_max_speed = Column(Numeric(precision=5, scale=3))
    max_speed = Column(Integer)
    avg_power = Column(Integer)
    max_power = Column(Integer)
    total_ascent = Column(Integer)
    total_descent = Column(Integer)
    start_position_lat_sem = Column(Integer)
    start_position_long_sem = Column(Integer)
    start_position_lat_deg = Column(Numeric(precision=8, scale=6))
    start_position_long_deg = Column(Numeric(precision=9, scale=6))
    start_location = Column(String)


    # avg_heart_rate = models.IntegerField(null=True)
    # max_heart_rate = models.IntegerField(null=True)

    file = relationship("ActivityFile", back_populates="activity_session")
