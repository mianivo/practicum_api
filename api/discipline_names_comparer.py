import spacy
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("ru_core_news_sm")


def get_vector(text):
    doc = nlp(text)
    return doc.vector


def compare_strings(string1, string2):
    vector1 = get_vector(string1)
    vector2 = get_vector(string2)
    similarity = cosine_similarity([vector1], [vector2])[0][0]
    return similarity


def calculate_comparison_percentage(disciplines, user_disciplines):
    names = set(discipline[0] for discipline in disciplines)
    user_discipline_names = set(discipline["name"] for discipline in user_disciplines)
    scores = {user_d_name: ["", 0] for user_d_name in user_discipline_names}
    for user_d_name in user_discipline_names:
        if type(user_d_name) != str:
            raise ValueError("Имя дисциплины должно быть строкой")
        for d_name in names:
            score = compare_strings(user_d_name, d_name)
            if score > scores[user_d_name][1]:
                scores[user_d_name] = [d_name, score]
    return scores
