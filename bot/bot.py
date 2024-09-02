import asyncio
import logging
from http import HTTPStatus

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault

from constants import BOT_TOKEN
from utils import get_product_description, get_product_info

dp = Dispatcher()
router = Router(name=__name__)
dp.include_router(router)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply('Введите nm_id товара, чтобы получить информацию.')


@router.message()
async def handle_product_request(message: types.Message):
    if message.text.isdigit():
        nm_id = message.text
        response = await get_product_description(nm_id)

        if response is None or response['status'] != HTTPStatus.OK:
            await message.reply('Ошибка получения данных. Попробуйте позже.')
            return

        product_info = get_product_info(response)

        await message.reply(product_info)
    else:
        await message.reply('Пожалуйста, введите корректный nm_id (число).')


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    if not BOT_TOKEN or not isinstance(BOT_TOKEN, str):
        logging.error("BOT_TOKEN должен быть передан.")
        return

    bot = Bot(
        token=BOT_TOKEN,
    )

    await bot.delete_webhook()
    await set_commands(bot)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except Exception as e:
        logging.exception(e)
