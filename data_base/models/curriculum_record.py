from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from data_base.models.base import Base


class CurriculumRecord(Base):
    __tablename__ = 'curriculum_records'

    id = Column(String, primary_key=True)

    discipline_title = Column(String)
    curriculum_id = Column(String, ForeignKey('curriculums.id'))
    testUnits = Column(Integer)

    curriculum = relationship('Curriculum', back_populates='curriculum_records')
    semester_controls = relationship('SemesterControls', back_populates='curriculum_record')

# сформировать таблицы ещё 40 минут
# распарсить данные в таблицу - 1 час
# Подумай над архитектурой апи. Будет ли два или три микросервиса, или будет хранить всё один сервис (вообще, напрашивается, что один)?
# как система будет справляться с высокой нагрузкой? Если одновременно куча запросов, что делать?
# (впрочем предыдущий пункт не так важен, т.к. я плохо представляю, в честь чего на сервер пойдёт высокая нагрузка (ddos?))
# разобраться с векоризацией после того, как сделаешь лабу по дата сайнс