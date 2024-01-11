def check_required_keys(key_list, input_dict):
    missing_keys = []
    for key in key_list:
        if key not in input_dict:
            print(key, key in input_dict, input_dict)
            missing_keys.append(key)
    return missing_keys


def check_main_key_names(input_json):
    missing_keys = check_required_keys(["direction_name", "semestr", "diciplines"], input_json)
    if missing_keys:
        raise KeyError(f'JSON файл содержит не все обязательные ключи.'
                       f' Список пропущенных ключей: {str(missing_keys)}')
    return True


def check_main_values_types(input_json):
    if type(input_json["direction_name"]) != str:
        raise ValueError("Имя направления должно быть строкой")
    if type(input_json["semestr"]) != int:
        raise ValueError("Номер семестра на который студент переводится должен быть строкой")
    if type(input_json["diciplines"]) != list:
        raise ValueError("По ключу diciplines дожен содержаться список дисциплин."
                         "Каждая дисциплина должна быть словарем формата: "
                         '{"name": "имя дисциплины", "hours": количество часов, "semestr":'
                         ' номер семестра, "is_exam": true/false}')


def check_list_item_keys(discipline_dict):
    missing_keys = check_required_keys(["name", "hours", "semestr", "is_exam"], discipline_dict)
    return missing_keys


def check_list_item_types(discipline_dict):
    if type(discipline_dict["name"]) != str:
        raise ValueError("Имя дисциплины в списке дисциплин должно быть строкой")
    if type(discipline_dict["hours"]) != int:
        raise ValueError("Количество зачетных едениц должно быть целым числом")
    if type(discipline_dict["semestr"]) != int:
        raise ValueError("Номер семестра должен быть целым числом")
    if type(discipline_dict["is_exam"]) != bool:
        raise ValueError("is_exam должно быть true или false")


def check_disciplines(input_json):
    for i, discipline in enumerate(input_json["diciplines"]):
        missing_keys = check_required_keys(["name", "hours", "semestr", "is_exam"], discipline)
        if missing_keys:
            raise ValueError(f"Дисциплина под номером {i} не содержит один или несколько ключей. "
                             f"Пропущенные ключи: {missing_keys}")
        check_list_item_types(discipline)


def check_user_input(input_json):
    check_main_key_names(input_json)
    check_main_values_types(input_json)
    check_disciplines(input_json)
