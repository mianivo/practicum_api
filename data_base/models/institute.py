from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class Institute(Base):
    __tablename__ = 'institutes'

    id = Column(String, primary_key=True)
    uuid = Column(String)
    title = Column(String)

    directions = relationship('Direction', back_populates='institute')