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


    ALL_PROGRAMMS_URL = "https://upop-api.my1.urfu.ru/programs"

    def prepare_chair(chair: dict, db_sess: Session) -> Chair:
        if chair is None:
            return None

        old_chair = db_sess.query(Chair).filter(Chair.id == chair["id"]).first()
        if old_chair:
            return old_chair

        new_chair = Chair()
        new_chair.id = chair["id"]
        new_chair.uuid = chair["uuid"]
        new_chair.title = chair["title"]
        return new_chair

    def prepare_institute(institute: dict, db_sess: Session) -> Institute:
        if institute is None:
            return None

        old_institute = db_sess.query(Institute).filter(Institute.id == institute["id"]).first()
        if old_institute:
            return old_institute

        new_institute = Institute()
        new_institute.id = institute["id"]
        new_institute.uuid = institute["uuid"]
        new_institute.title = institute["title"]
        return new_institute

    def prepare_employee(employee: dict, db_sess: Session) -> Employee:
        if employee is None:
            return None

        old_employee = db_sess.query(Employee).filter(Employee.id == employee["employeeId"]).first()
        if old_employee:
            return old_employee

        new_employee = Employee()
        new_employee.id = employee["employeeId"]
        new_employee.person_id = employee["personId"]
        new_employee.username = employee["username"]
        new_employee.fullname = employee["fullname"]
        db_sess.add(new_employee)
        db_sess.commit()
        return new_employee


    def prepare_direction(direction: dict, db_sess: Session) -> Direction:
        old_direction = db_sess.query(Direction).filter(Direction.id == direction["id"]).first()
        if old_direction:
            return

        new_direction = Direction()
        new_direction.id = direction["id"]
        new_direction.uniId = direction["uniId"]
        new_direction.status = direction["status"]
        new_direction.name = direction["name"]
        new_direction.level = direction["level"]
        new_direction.startYear = direction["startYear"]
        new_direction.cypher = direction["cypher"]

        chair = prepare_chair(direction["chair"], db_sess)
        institute = prepare_institute(direction["institute"], db_sess)
        head = prepare_employee(direction["head"], db_sess)
        site_admin = prepare_employee(direction["siteAdmin"], db_sess)

        new_direction.chair = chair
        new_direction.institute = institute
        new_direction.head = head
        new_direction.site_admin = site_admin
        db_sess.add(new_direction)
        db_sess.commit()


    db_sess = create_session()
    all_programs = requests.get(ALL_PROGRAMMS_URL).json()
    for short_direction_info in all_programs:
        program_id = short_direction_info["id"]
        full_direction_info = requests.get(ALL_PROGRAMMS_URL + f"/{program_id}").json()
        prepare_direction(full_direction_info, db_sess)
