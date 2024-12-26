def generate_result_message(result):
    animals = {
        "Ёжик": "Интроверт, любящий тишину.",
        "Тигр": "Смелый лидер.",
        "Выдра": "Дружелюбный заботливый друг.",
        "Обезьяна": "Активный и энергичный."
    }
    animal = list(animals.keys())[result]
    return (f"Ваше тотемное животное — {animal}!\n{animals[animal]}\n"
            f"Узнайте больше о программе опеки: https://moscowzoo.ru/opportunities/patronage/")