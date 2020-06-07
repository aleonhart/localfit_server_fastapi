# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
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
    start_time_utc = Column(DateTime)
    # start_position_lat_sem = models.IntegerField(null=True)
    # start_position_long_sem = models.IntegerField(null=True)
    # start_position_lat_deg = models.DecimalField(null=True, max_digits=8, decimal_places=6)
    # start_position_long_deg = models.DecimalField(null=True, max_digits=9, decimal_places=6)
    # start_location = models.CharField(null=True, max_length=200)
    # total_elapsed_time = models.DecimalField(null=True, max_digits=10, decimal_places=3)
    # total_timer_time = models.DecimalField(null=True, max_digits=10, decimal_places=3)
    # total_distance = models.DecimalField(null=True, max_digits=8, decimal_places=2)
    # total_strides = models.IntegerField(null=True)
    # total_cycles = models.IntegerField(null=True)
    # total_calories = models.IntegerField(null=True)
    # enhanced_avg_speed = models.DecimalField(null=True, max_digits=5, decimal_places=3)
    # avg_speed = models.IntegerField(null=True)
    # enhanced_max_speed = models.DecimalField(null=True, max_digits=5, decimal_places=3)
    # max_speed = models.IntegerField(null=True)
    # avg_power = models.IntegerField(null=True)
    # max_power = models.IntegerField(null=True)
    # total_ascent = models.IntegerField(null=True)
    # total_descent = models.IntegerField(null=True)
    # avg_heart_rate = models.IntegerField(null=True)
    # max_heart_rate = models.IntegerField(null=True)

    file = relationship("ActivityFile", back_populates="activity_session")
