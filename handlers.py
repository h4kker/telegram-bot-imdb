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
        The bot allows you to query movies with the lowest and highest ratings, 
        as well as query movies in a custom rating range.
        It also keeps a history of the last 10 queries for each user."""
    )

    text = f"""
    {message.from_user.first_name}, you can use the following commands:
    1. Query movies with the lowest rating (command /low).
    2. Query movies with the highest rating (command /high).
    3. Query movies in a custom range (command /custom <start> <end>).
    4. View your query history (command /history).
    """
    await message.answer(text=text)


@router.message(Command("help"))
async def command_help_handler(message: Message):
    text = f"""
{message.from_user.first_name}, you can use the following commands to interact with the bot:
1. Query movies with the lowest rating (command /low).
2. Query movies with the highest rating (command /high).
3. Query a custom range of movies (command /custom 10 20).
4. View the history of your requests (command /history).
"""
    await message.answer(text=text)


@router.message(Command("low"))
async def command_low_handler(message: Message) -> None:
    add_to_history(message.from_user.id, "/low")
    data = await fetch_movies()

    if "error" in data:
        await message.answer(text=f"Error: {data['error']}")
        return

    if isinstance(data, list):
        if len(data) >= 10:
            movie_list = "\n".join(
                [
                    f"{len(data) - 10 + i + 1}. {movie['title']} ({movie['year']})"
                    for i, movie in enumerate(data[-10:])
                ]
            )
            await message.answer(
                text=f"10 movies with the lowest ratings:\n{movie_list}"
            )
        else:
            await message.answer(text="The list contains insufficient movies.")
    else:
        await message.answer(text=f"Error: {data.get('error', 'invalid data from the API.')}")


@router.message(Command("high"))
async def command_high_handler(message: Message) -> None:
    add_to_history(message.from_user.id, "/high")
    data = await fetch_movies()

    if "error" in data:
        await message.answer(text=f"Error: {data['error']}")
        return

    if isinstance(data, list):
        if len(data) >= 10:
            movie_list = "\n".join(
                [
                    f"{i + 1}. {movie['title']} ({movie['year']})"
                    for i, movie in enumerate(data[:10])
                ]
            )
            await message.answer(
                text=f"10 movies with the lowest ratings:\n{movie_list}"
            )
        else:
            await message.answer(text="The list contains insufficient movies..")
    else:
        await message.answer(text=f"Error: {data.get('error', 'invalid data from the API.')}")


@router.message(Command("custom"))
async def command_custom_handler(message: Message) -> None:
    args = message.text.split()

    if len(args) == 3:
        try:
            start = int(args[1]) - 1
            end = int(args[2])
            data = await fetch_movies()
            if start > end:
                await message.answer(
                    text="The starting number should be less than the ending number."
                )
                await message.answer(
                    text="Please enter two numbers for the range, e.g., /custom 1 10."
                )
                return
            elif start < 0 or end < 0:
                await message.answer(
                    text="The starting and ending numbers must be positive."
                )
                return
            elif isinstance(data, list):
                if start < 0 or end > len(data):
                    await message.answer(
                        text="The range exceeds the available movies."
                    )
                    return

                movie_list = "\n".join(
                    [
                        f"{i + 1}. {movie['title']} ({movie['year']})"
                        for i, movie in enumerate(data[start:end])
                    ]
                )
                await message.answer(
                    text=f"Movies in the range from {start + 1} to {end}:\n{movie_list}"
                )
                add_to_history(message.from_user.id, f"/custom {args[1]} {args[2]}")
            else:
                await message.answer(
                    text=f"Error: {data.get('error', 'invalid data from the API.')}"
                )
        except ValueError:
            await message.answer(
                text="Please enter two numbers for the range, e.g., /custom 1 10."
            )
    else:
        await message.answer(
            text="The command should include two numbers for the range, e.g., /custom 1 10."
        )


@router.message(Command("history"))
async def command_history_handler(message: Message) -> None:
    history = get_user_history(message.from_user.id)
    if history:
        history_text = "\n".join(
            [
                f"{i + 1}. {cmd} — {timestamp}"
                for i, (cmd, timestamp) in enumerate(history)
            ]
        )
        await message.answer(
            text=f"Your last 10 queries:\n{history_text}"
        )
    else:
        await message.answer(text="Your query history is empty.")
