from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class Direction(Base):
    __tablename__ = 'directions'

    id = Column(Integer, primary_key=True)
    uniId = Column(String, primary_key=True)
    status = Column(String)
    name = Column(String)
    level = Column(String)
    startYear = Column(Integer)
    cypher = Column(String)

    curriculum = relationship('Curriculum', back_populates='direction')


    chair_id = Column(String, ForeignKey('chairs.id'), nullable=True)
    chair = relationship('Chair', back_populates='directions')

    institute_id = Column(String, ForeignKey('institutes.id'), nullable=True)
    institute = relationship('Institute', back_populates='directions')

    head_id = Column(String, ForeignKey('employees.id'), nullable=True)
    head = relationship('Employee', foreign_keys=[head_id])

    site_admin_id = Column(String, ForeignKey('employees.id'), nullable=True)
    site_admin = relationship('Employee',foreign_keys=[site_admin_id])

