from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class Curriculum(Base):
    __tablename__ = 'curriculums'

    id = Column(String, primary_key=True) # plan
    plan_title = Column(String)
    version = Column(String)
    version_title = Column(String)

    index = Column(String)

    curriculum_records = relationship('CurriculumRecord', back_populates='curriculum')

    direction_id = Column(Integer, ForeignKey('directions.id'))
    direction = relationship('Direction', back_populates='curriculum')