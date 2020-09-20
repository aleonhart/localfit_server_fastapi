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
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)

    """
    RELATIONSHIPS
    
    backref: 
        establishes relationship: ActivityFile.activity_records 
        establishes relationship: ActivityRecord.activity_file
    
    cascade:
        save-update: Default behavior. Indicates that when an object is placed into a Session via Session.add(), all 
            the objects associated with it via this relationship() should also be added to that same Session.
        merge: Default behavior. Indicates that the Session.merge() operation should be propagated from a parent that’s 
            the subject of the Session.merge() call down to referred objects. 
        delete: Indicates that when a “parent” object is marked for deletion, its related “child” objects should also 
            be marked for deletion.
    """
    activity_records = relationship("ActivityRecord", backref="activity_file", cascade="save-update, merge, delete")


class ActivityRecord(Base):
    __tablename__ = "activity_record"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("activity_file.id"))
    timestamp_utc = Column(DateTime, nullable=False)
    heart_rate = Column(Integer)                                # BPM
    position_lat_sem = Column(Integer)                          # semicircles
    position_long_sem = Column(Integer)                         # semicircles
    position_lat_deg = Column(Numeric(precision=8, scale=6))    #      XX.XXXXXX degrees
    position_long_deg = Column(Numeric(precision=9, scale=6))   #     XXX.XXXXXX degrees
    distance = Column(Numeric(precision=8, scale=2))            # XXX,XXX.XX  meters, 100mi is 160,934m
    altitude = Column(Numeric(precision=5, scale=1))            #   X,XXX.X   meters, Mt. Everest is 8,850m high
    speed = Column(Integer)                                     #      XX     meters/second, Usain Bolt's top speed is 12.27m/s
    cadence = Column(Integer)                                   # RPM
    fractional_cadence = Column(Numeric(precision=5, scale=1))  # RPM
    enhanced_altitude = Column(Numeric(precision=5, scale=1))   #   X,XXX.X   meters
    enhanced_speed = Column(Numeric(precision=5, scale=3))      #      XX.XXX meters/second
