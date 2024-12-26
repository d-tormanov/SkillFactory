from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.logger_config import logger
from utils.quiz_logic import QUESTIONS, calculate_result
from utils.result_handler import generate_result_message

router = Router()
user_answers = {}


def register_handlers(dp):
    dp.include_router(router)


@router.message(Command("quiz"))
async def quiz_start(message: Message):
    """Начало викторины."""
    logger.info(f"Команда /quiz вызвана пользователем {message.from_user.id}")
    user_answers[message.from_user.id] = []
    question = QUESTIONS[0]["question"]
    options = QUESTIONS[0]["options"]

    # Формируем клавиатуру, извлекая текст из словаря "answer"
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

        # Добавляем кнопку для перезапуска
        restart_button = InlineKeyboardButton(text="Попробовать ещё раз?", callback_data="restart_quiz")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[restart_button]])

        # Отправляем результат с кнопкой для перезапуска
        await callback_query.message.edit_text(result_message, reply_markup=keyboard)
        del user_answers[user_id]


@router.callback_query(lambda c: c.data == "restart_quiz")
async def restart_quiz(callback_query: CallbackQuery):
    """Перезапуск викторины."""
    user_id = callback_query.from_user.id
    logger.info(f"Пользователь {user_id} хочет перезапустить викторину.")

    # Перезапускаем викторину, очищая ответы пользователя
    user_answers[user_id] = []

    # Отправляем первый вопрос с кнопками
    question = QUESTIONS[0]["question"]
    options = QUESTIONS[0]["options"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=option["answer"], callback_data=f"quiz_0_{idx}")]
        for idx, option in enumerate(options)
    ])

    await callback_query.message.edit_text(question, reply_markup=keyboard)
