from data_base.session import create_session

from data_base.models.direction import Direction

from data_base.models.curriculum import Curriculum
from data_base.models.curriculum_record import CurriculumRecord

from api.discipline_names_comparer import calculate_comparison_percentage

MINIMAL_SCORE = 0.9


def get_disciplines(direction_name, semestr):
    db_sess = create_session()
    direction = db_sess.query(Direction).filter(Direction.name == direction_name).first()
    if not direction:
        raise ValueError(f"Нет направления с названием {str(direction_name)}")
    curriculum = db_sess.query(Curriculum).filter(Curriculum.direction_id == direction.id).first()
    disciplines = db_sess.query(CurriculumRecord).filter(CurriculumRecord.curriculum_id == curriculum.id).all()

    data = [[i.discipline_title, j.test_units, j.is_exam, j.semester] for i in disciplines for j in i.semester_controls
            if j.semester <= semestr]
    data = list(filter(lambda x: bool(x), data))
    return data


def form_answer_record(user_discipline, discipline, academy_credit):
    return {"user_discipline": user_discipline, "direction_discipline": discipline, "academy_credit": academy_credit}


def calculate_academy_credit(direction_name, semestr, user_disciplines):
    disciplines = get_disciplines(direction_name, semestr)
    scores = calculate_comparison_percentage(disciplines, user_disciplines)
    answer = []
    was_disciplines = []
    for user_discipline in user_disciplines:
        if scores[user_discipline["name"]][1] < MINIMAL_SCORE:
            answer.append(form_answer_record(user_discipline, None, 0))
        else:
            for discipline in filter(lambda d: d[0] == scores[user_discipline["name"]][0], disciplines):
                if user_discipline["is_exam"] < discipline[2]:
                    answer.append(form_answer_record(user_discipline, discipline, discipline[1]))
                elif user_discipline["semestr"] < discipline[3]:
                    answer.append(form_answer_record(user_discipline, discipline, discipline[1]))
                else:
                    answer.append(form_answer_record(user_discipline, discipline,
                                                     max(0, user_discipline["hours"] - discipline[1])))
                was_disciplines.append(discipline)
    for discipline in disciplines:
        if discipline in was_disciplines:
            continue
        answer.append(form_answer_record(None, discipline, discipline[1]))

    return {"compare": answer, "academy_credit": sum([record["academy_credit"] for record in answer])}
