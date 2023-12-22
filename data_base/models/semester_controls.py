from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class SemesterControls(Base):
    __tablename__ = 'semester_controls'

    id = Column(Integer, primary_key=True, autoincrement=True)

    record_id = Column(String, ForeignKey('curriculum_records.id'))
    semester = Column(Integer)
    is_exam = Column(Boolean)
    test_units = Column(Integer)

    curriculum_record = relationship('CurriculumRecord', back_populates='semester_controls')