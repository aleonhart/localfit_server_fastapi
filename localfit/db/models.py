# SQLAlchemy models

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from localfit.db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)


# class ActivityType(Base):
#     __tablename__ = "activity_type"
#     activity_type = Column(String)


class ActivityFile(Base):
    __tablename__ = "activity_type"
    id = Column(Integer, primary_key=True)
    filename = Column(String, unique=True)
    # activity_type = Column(String)
    # activity_category = Column(String)
    # activity_collection = Column(String)
    # start_time_utc = Column(DateTime)
    # primary_file = Column(Boolean, default=True)
    #secondary_activity = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
