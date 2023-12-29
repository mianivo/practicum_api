import requests
from sqlalchemy.orm import Session
from data_base import session

from data_base.session import create_session, global_init

global_init("../test.sqlite")

from data_base.models.direction import Direction
from data_base.models.chair import Chair
from data_base.models.institute import Institute
from data_base.models.employee import Employee
from data_base.models.curriculum import Curriculum
from data_base.models.curriculum_record import CurriculumRecord
from data_base.models.semester_controls import SemesterControls
import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("ru_core_news_sm")
MINIMAL_SCORE = 0.9


def get_vector(text):
    doc = nlp(text)
    return doc.vector


def compare_strings(string1, string2):
    vector1 = get_vector(string1)
    vector2 = get_vector(string2)
    similarity = cosine_similarity([vector1], [vector2])[0][0]
    return similarity


def get_disciplines(direction_name, semestr):
    db_sess = create_session()
    direction = db_sess.query(Direction).filter(Direction.name == direction_name).first()
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
    names = set(discipline[0] for discipline in disciplines)
    user_discipline_names = set(discipline["name"] for discipline in user_disciplines)
    scores = {user_d_name: ["", 0] for user_d_name in user_discipline_names}
    for user_d_name in user_discipline_names:
        for d_name in names:
            score = compare_strings(user_d_name, d_name)
            if score > scores[user_d_name][1]:
                scores[user_d_name] = [d_name, score]
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




calculate_academy_credit("Программная инженерия", 1,
                         [{"name": 'История России', "hours": 3, "semestr": 1, "is_exam": False},
                          {"name": 'Математика', "hours": 4, "semestr": 1, "is_exam": True},
                          {"name": 'Физика', "hours": 4, "semestr": 1, "is_exam": True},
                          {"name": 'Английский язык', "hours": 4, "semestr": 1, "is_exam": False},
                          {"name": 'Физическая культура', "hours": 2, "semestr": 1, "is_exam": False},
                          {"name": 'Физическая культура', "hours": 2, "semestr": 2, "is_exam": False}, ])

