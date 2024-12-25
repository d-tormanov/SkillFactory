import random
import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from deep_translator import GoogleTranslator
import aiohttp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

translator = GoogleTranslator(source='en', target='ru')


async def get_categories():
    url = "http://www.themealdb.com/api/json/v1/1/list.php?c=list"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return [category['strCategory'] for category in data['meals']]


async def get_recipes_by_category(category):
    url = f"http://www.themealdb.com/api/json/v1/1/filter.php?c={category}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data['meals']


async def get_recipe_details(recipe_id):
    url = f"http://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data['meals'][0]


async def send_recipe_message(message: Message, recipe_details):
    for details in recipe_details:
        recipe_name = translator.translate(details["strMeal"])
        recipe_instructions = translator.translate(details["strInstructions"])

        recipe_ingredients = [
            translator.translate(details.get(f"strIngredient{i}"))
            for i in range(1, 21) if details.get(f"strIngredient{i}")
        ]

        ingredient_text = "\n".join(recipe_ingredients)

        recipe_message = (
            f"Рецепт: {recipe_name}\n\n"
            f"Ингредиенты:\n{ingredient_text}\n\n"
            f"Инструкция:\n{recipe_instructions}"
        )

        await message.answer(recipe_message, reply_markup=ReplyKeyboardRemove())


async def category_search_start(message: Message, state: FSMContext):
    """ Обработчик для команды /category_search_random """

    logger.debug(f"Received command: {message.text}")

    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.answer(
                "Пожалуйста, укажите количество рецептов после команды. Например: /category_search_random 3")
            return

        num_recipes = int(command_parts[1])
        await state.update_data(num_recipes=num_recipes)

        categories = await get_categories()
        logger.debug(f"Fetched categories: {categories}")

        buttons = [KeyboardButton(text=cat) for cat in categories]
        keyboard = ReplyKeyboardMarkup(keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)],
                                       resize_keyboard=True)
        await message.answer("Выберите категорию:", reply_markup=keyboard)

        await state.update_data(categories=categories)

    except (ValueError, IndexError) as e:
        logger.error(f"Error in category_search_start: {e}")
        await message.answer("Введите число рецептов после команды.")


async def choose_category(message: Message, state: FSMContext):
    """ Обработчик для выбора категории """

    logger.debug(f"User selected category: {message.text}")

    data = await state.get_data()
    categories = data.get('categories')

    if not categories:
        await message.answer("Сначала выполните команду /category_search_random, чтобы получить список категорий.")
        return

    category = message.text.strip()
    logger.debug(f"Category selected by user: {category}")

    if category not in categories:
        logger.warning(f"Invalid category: {category}")
        await message.answer("Вы выбрали неверную категорию. Попробуйте снова.")
        return

    await state.update_data(selected_category=category)

    await message.answer("Загружаем рецепты...")

    recipes = await get_recipes_by_category(category)
    if not recipes:
        await message.answer("Для этой категории нет доступных рецептов.")
        return

    num_recipes = (await state.get_data()).get("num_recipes", 1)
    chosen_recipes = random.choices(recipes, k=num_recipes)

    recipe_details = []
    for recipe in chosen_recipes:
        recipe_id = recipe["idMeal"]
        details = await get_recipe_details(recipe_id)
        recipe_details.append(details)

    await send_recipe_message(message, recipe_details)


async def fetch_recipes(message: Message, state: FSMContext):
    """ Обработчик для получения рецептов """

    logger.debug(f"Fetching recipes for category: {message.text}")

    data = await state.get_data()
    category = data.get('selected_category')
    num_recipes = data.get("num_recipes", 1)

    if not category:
        await message.answer("Сначала выберите категорию!")
        return

    recipes = await get_recipes_by_category(category)
    chosen_recipes = random.choices(recipes, k=num_recipes)

    recipe_details = []
    for recipe in chosen_recipes:
        recipe_id = recipe["idMeal"]
        details = await get_recipe_details(recipe_id)
        recipe_details.append(details)

    await send_recipe_message(message, recipe_details)


def register_handlers(router: Router):
    """  Регистрация обработчиков """

    router.message.register(category_search_start, Command("category_search_random"))
    router.message.register(choose_category, F.text)
    router.message.register(fetch_recipes, F.text)
