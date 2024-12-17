from typing import Dict

from catboost import CatBoostClassifier

from app.config import settings
from app.utils.base_model import singleton


@singleton
class MultiClassifier:
    LABEL_TO_CLASS = {
        0: "Личные документы",
        1: "Здоровье",
        2: "Социальная поддержка",
        3: "Справки и выписки",
        4: "Транспорт",
        5: "Финансы, налоги, штрафы",
        6: "Семья",
        7: "Пенсия",
        8: "Образование",
        9: "Работа",
        10: "Бизнес",
        11: "Недвижимость",
        12: "Правопорядок",
        13: "Спорт, культура и путешествия",
        14: "Оружие, охота, рыбалка",
        15: "Интернет и связь",
        16: "Иностранным гражданам",
    }

    def __init__(self):
        self.empty_model = CatBoostClassifier()
        self.model = self.empty_model.load_model(settings.MULTI_CLASSIFIER_CBM)

    def predict(self, text: str) -> str:
        label = self.model.predict([text])
        return self.LABEL_TO_CLASS.get(label[0])
