from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class Chair(Base):
    __tablename__ = 'chairs'

    id = Column(String, primary_key=True)
    uuid = Column(String)
    title = Column(String)

    directions = relationship('Direction', back_populates='chair')