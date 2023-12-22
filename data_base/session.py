import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from data_base.models.base import Base

from data_base.models.chair import Chair
from data_base.models.curriculum import Curriculum
from data_base.models.curriculum_record import CurriculumRecord
from data_base.models.semester_controls import SemesterControls
from data_base.models.direction import Direction
from data_base.models.employee import Employee
from data_base.models.institute import Institute

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
