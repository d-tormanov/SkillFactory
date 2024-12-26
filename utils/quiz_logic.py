QUESTIONS = [
    {
        "question": "Как вы предпочитаете проводить свободное время?",
        "options": [
            {"answer": "Одиночество", "weight": 1},
            {"answer": "С друзьями", "weight": 2},
            {"answer": "На природе", "weight": 3},
            {"answer": "В движении", "weight": 4}
        ]
    },
    {
        "question": "Какое ваше главное качество?",
        "options": [
            {"answer": "Терпение", "weight": 1},
            {"answer": "Смелость", "weight": 2},
            {"answer": "Дружелюбие", "weight": 3},
            {"answer": "Энергичность", "weight": 4}
        ]
    },
    # Добавить больше вопросов
]


RESULTS = {
    0: "Ёжик",
    1: "Тигр",
    2: "Выдра",
    3: "Обезьяна"
}

def calculate_result(answers):
    scores = [0] * len(RESULTS)

    for i, answer in enumerate(answers):
        question = QUESTIONS[i]
        weight = question["options"][answer]["weight"]
        scores[answer] += weight

    return scores.index(max(scores))
