if __name__ == "__main__":
    import requests
    from sqlalchemy.orm import Session
    from data_base import session

    session.global_init("../test.sqlite")

    from data_base.session import create_session

    from data_base.models.direction import Direction
    from data_base.models.chair import Chair
    from data_base.models.institute import Institute
    from data_base.models.employee import Employee
    from data_base.models.curriculum import Curriculum
    from data_base.models.curriculum_record import CurriculumRecord
    from data_base.models.semester_controls import SemesterControls

    import pandas as pd

    files = ['eduplan_1.csv', "eduplan_2.csv"]

    data_list = []
    db_sess = create_session()
    for file in files:
        data = pd.read_csv(file, sep=';')
        first_row = data.iloc[0]

        new_cirriclum = db_sess.query(Curriculum).filter(Curriculum.id == first_row["plan"]).first()
        if not new_cirriclum:
            new_cirriclum = Curriculum()
            new_cirriclum.id = first_row["plan"]
            new_cirriclum.plan_title = first_row["planTitle"]
            new_cirriclum.version = first_row["version"]
            new_cirriclum.version_title = first_row["versionTitle"]
            new_cirriclum.index = first_row["index"]

            direction = db_sess.query(Direction).filter(Direction.cypher == first_row["profileCode"]).first()
            new_cirriclum.direction = direction
            db_sess.add(new_cirriclum)
            db_sess.commit()

        parent_graph = {}
        data = data.fillna(0)

        for ind in range(len(data)):
            row = data.iloc[ind]
            parent_graph[row["id"]] = row["parent"]
            if not row["controls_list"]:
                continue
            if (parent_graph[row["id"]] == 0) or (parent_graph[parent_graph[row["id"]]] == 0):
                continue
            new_curriculum_record = db_sess.query(CurriculumRecord).filter(CurriculumRecord.id == row["id"]).first()
            if new_curriculum_record:
                continue
            new_curriculum_record = CurriculumRecord()
            new_curriculum_record.id = row["id"]
            new_curriculum_record.discipline_title = row["title"]
            new_curriculum_record.testUnits = int(row["testUnits"])
            new_curriculum_record.curriculum = new_cirriclum
            db_sess.add(new_curriculum_record)
            db_sess.commit()

            semesters = [(row[col], ind) for col, ind in [(f"ttu{sem}", sem) for sem in range(1, 13)] if row[col] != 0]
            exam_dict = {k:(v == "Экзамен") for (k, v) in [i.split(':') for i in row["controls_list"].split(',')]}
            for hours, sem_number in semesters:
                new_semester_control = SemesterControls()
                new_semester_control.semester = sem_number
                new_semester_control.test_units = int(hours)
                new_semester_control.is_exam = exam_dict[str(sem_number)]
                new_semester_control.curriclum_record = new_curriculum_record
                new_semester_control.record_id = new_curriculum_record.id
                db_sess.add(new_semester_control)
                db_sess.commit()
