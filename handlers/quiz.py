from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types.input_file import FSInputFile
from utils.logger_config import logger
from utils.quiz_logic import QUESTIONS, calculate_result
from utils.result_handler import generate_result_message
import os

router = Router()
user_answers = {}

IMAGE_PATH = "images/"
ANIMAL_IMAGES = {
    0: "hedgehog.jpeg",   # Ёжик
    1: "tiger.jpeg",      # Тигр
    2: "otter.jpeg",      # Выдра
    3: "monkey.jpeg",     # Обезьяна
}

def register_handlers(dp):
    dp.include_router(router)


@router.message(Command("quiz"))
async def quiz_start(message: Message):
    """Начало викторины."""
    logger.info(f"Команда /quiz вызвана пользователем {message.from_user.id}")
    user_answers[message.from_user.id] = []
    question = QUESTIONS[0]["question"]
    options = QUESTIONS[0]["options"]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=option["answer"], callback_data=f"quiz_0_{idx}")]
        for idx, option in enumerate(options)
    ])

    await message.answer(question, reply_markup=keyboard)


@router.callback_query(lambda c: c.data.startswith("quiz"))
async def quiz_answer(callback_query: CallbackQuery):
    """Обработка ответов викторины."""
    data = callback_query.data.split("_")
    question_idx, answer_idx = int(data[1]), int(data[2])
    user_id = callback_query.from_user.id
    logger.info(f"Ответ пользователя {user_id}: Вопрос {question_idx}, Ответ {answer_idx}")

    user_answers[user_id].append(answer_idx)

    if question_idx + 1 < len(QUESTIONS):
        next_question = QUESTIONS[question_idx + 1]["question"]
        options = QUESTIONS[question_idx + 1]["options"]

        # Формируем клавиатуру для следующего вопроса
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=option["answer"], callback_data=f"quiz_{question_idx + 1}_{idx}")]
            for idx, option in enumerate(options)
        ])

        await callback_query.message.edit_text(next_question, reply_markup=keyboard)
    else:
        result = calculate_result(user_answers[user_id])
        result_message = generate_result_message(result)
        logger.info(f"Результат для пользователя {user_id}: {result_message}")

        await callback_query.message.delete()

        # Отправка изображения в зависимости от результата
        animal_image = ANIMAL_IMAGES.get(result)
        if animal_image:
            image_path = os.path.join(IMAGE_PATH, animal_image)
            if os.path.exists(image_path):

                image_file = FSInputFile(image_path, filename=animal_image)

                result_msg = await callback_query.message.answer_photo(
                    image_file,
                    caption=result_message  # Текст под картинкой
                )

                # Добавляем кнопку для перезапуска
                restart_button = InlineKeyboardButton(text="Попробовать ещё раз?", callback_data="restart_quiz")
                keyboard = InlineKeyboardMarkup(inline_keyboard=[[restart_button]])

                await result_msg.edit_reply_markup(reply_markup=keyboard)
            else:
                logger.error(f"Изображение не найдено: {image_path}")
                await callback_query.message.answer(result_message)
        else:
            await callback_query.message.answer(result_message)

        # Удаляем данные пользователя после завершения викторины
        del user_answers[user_id]


@router.callback_query(lambda c: c.data == "restart_quiz")
async def restart_quiz(callback_query: CallbackQuery):
    """Перезапуск викторины."""
    user_id = callback_query.from_user.id
    logger.info(f"Пользователь {user_id} хочет перезапустить викторину.")

    # Перезапускаем викторину
    user_answers[user_id] = []
    await callback_query.message.delete()

    # Отправляем первый вопрос с кнопками
    question = QUESTIONS[0]["question"]
    options = QUESTIONS[0]["options"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=option["answer"], callback_data=f"quiz_0_{idx}")]
        for idx, option in enumerate(options)
    ])

    await callback_query.message.answer(question, reply_markup=keyboard)

