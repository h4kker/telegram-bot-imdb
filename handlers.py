from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram import Router
from api.init import fetch_movies
from database import add_to_history, get_user_history

router = Router()


@router.message(CommandStart())
async def start_message_handler(message: Message):
    await message.answer(
        text=f"""Hello {message.from_user.full_name}! 
    Бот позволяет выполнять запросы для получения списка фильмов с минимальными и максимальными рейтингами, а также запрашивать фильмы в пользовательском диапазоне рейтингов.
     Он также сохраняет историю последних 10 запросов для каждого пользователя"""
    )

    text = f"""
    {message.from_user.first_name} можете использовать следующие команды для работы с ботом:
    1. Запросить минимальные значения (команда /low).
    2. Запросить максимальные значения (команда /high).
    3. Запросить диапазон значений (команда /custom).
    4. Узнать историю запросов (команда /history).
    """
    await message.answer(text=text)


@router.message(Command("help"))
async def command_help_handler(message: Message):
    text = f"""
{message.from_user.first_name} можете использовать следующие команды для работы с ботом:
1. Запросить фильмы с наименьшим рейтингом (команда /low).
2. Запросить фильмы с наибольшим рейтингом (команда /high).
3. Запросить диапазон значений (команда /custom 10 20).
4. Узнать историю запросов (команда /history).
"""
    await message.answer(text=text)


@router.message(Command("low"))
async def command_low_handler(message: Message):
    add_to_history(message.from_user.id, "/low")
    data = await fetch_movies()

    if isinstance(data, list):
        if len(data) >= 10:
            movie_list = "\n".join(
                [
                    f"{len(data) - 10 + i + 1}. {movie['title']} ({movie['year']})"
                    for i, movie in enumerate(data[-10:])
                ]
            )
            await message.answer(
                text=f"10 фильмов с наименьшим рейтингом:\n{movie_list}"
            )
        else:
            await message.answer(text="В списке недостаточно фильмов.")
    else:
        await message.answer(text=f"Ошибка: {data.get('error', 'Неизвестная ошибка')}")


@router.message(Command("high"))
async def command_high_handler(message: Message):
    add_to_history(message.from_user.id, "/high")
    data = await fetch_movies()

    if isinstance(data, list):
        if len(data) >= 10:
            movie_list = "\n".join(
                [
                    f"{i + 1}. {movie['title']} ({movie['year']})"
                    for i, movie in enumerate(data[:10])
                ]
            )
            await message.answer(
                text=f"10 фильмов с наибольшим рейтингом:\n{movie_list}"
            )
        else:
            await message.answer(text="В списке недостаточно фильмов.")
    else:
        await message.answer(text=f"Ошибка: {data.get('error', 'Неизвестная ошибка')}")


@router.message(Command("custom"))
async def command_custom_handler(message: Message):
    args = message.text.split()

    if len(args) == 3:
        try:
            start = int(args[1]) - 1
            end = int(args[2])
            data = await fetch_movies()
            if start > end:
                await message.answer(
                    text="Начальное число должно быть меньше конечного."
                )
                await message.answer(
                    text="Пожалуйста, введите два числа для диапазона, например: /custom 1 10."
                )
                return
            elif start < 0 or end < 0:
                await message.answer(
                    text="Начальное и конечное числа должны быть положительными."
                )
                return
            elif isinstance(data, list):
                if start < 0 or end > len(data):
                    await message.answer(
                        text="Диапазон выходит за пределы доступных фильмов."
                    )
                    return

                movie_list = "\n".join(
                    [
                        f"{i + 1}. {movie['title']} ({movie['year']})"
                        for i, movie in enumerate(data[start:end])
                    ]
                )
                await message.answer(
                    text=f"Фильмы в диапазоне с {start + 1} по {end}:\n{movie_list}"
                )
                add_to_history(message.from_user.id, f"/custom {args[1]} {args[2]}")
            else:
                await message.answer(
                    text=f"Ошибка: {data.get('error', 'Неизвестная ошибка')}"
                )
        except ValueError:
            await message.answer(
                text="Пожалуйста, введите два числа для диапазона, например: /custom 1 10."
            )
    else:
        await message.answer(
            text="Команда должна содержать два числа для диапазона, например: /custom 1 10."
        )


@router.message(Command("history"))
async def command_history_handler(message: Message):
    history = get_user_history(message.from_user.id)
    if history:
        history_text = "\n".join(
            [
                f"{i + 1}. {cmd} — {timestamp}"
                for i, (cmd, timestamp) in enumerate(history)
            ]
        )
        await message.answer(
            text=f"История ваших последних 10 запросов:\n{history_text}"
        )
    else:
        await message.answer(text="История запросов пуста.")
