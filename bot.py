from __future__ import annotations

import asyncio
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WeatherBot.settings')

import django  # noqa: E402

django.setup()

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from users.models import User
from weather.models import WeatherRequest
from weather.services import WeatherAPIError, fetch_weather

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    print('TELEGRAM_BOT_TOKEN is not configured', file=sys.stderr)
    sys.exit(1)

bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message) -> None:
    await message.answer('Send /weather <city> to get the forecast')


@router.message(Command('weather'))
async def cmd_weather(message: Message) -> None:
    text = message.text or ''
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer('Usage: /weather <city>')
        return

    city = parts[1]
    try:
        data = await asyncio.to_thread(fetch_weather, city)
    except WeatherAPIError as exc:
        await message.answer(f'Error: {exc}')
        return

    user = User.objects.filter(telegram_id=str(message.from_user.id)).first()
    if user:
        WeatherRequest.objects.create(
            user=user,
            city=data.city,
            temperature=data.temperature,
            description=data.description,
            icon=data.icon,
        )

    reply = (
        f"<b>{data.city}</b>\n"
        f"Temperature: {data.temperature:.1f} °C\n"
        f"{data.description}"
    )
    await message.answer(reply)


dp.include_router(router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
