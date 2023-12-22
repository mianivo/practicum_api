from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True)
    person_id = Column(String)
    username = Column(String)
    fullname = Column(String)


