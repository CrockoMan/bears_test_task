import asyncio
import logging
from http import HTTPStatus

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault

from constants import (
    BOT_TOKEN, NEED_BOT_TOKEN, NEED_CORRECT_NM_ID, NEED_NM_ID, RESPONSE_ERROR,
    NOT_FOUND_ERROR
)
from utils import get_product_description, get_product_info


dp = Dispatcher()
router = Router(name=__name__)
dp.include_router(router)


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply(NEED_NM_ID)


@router.message()
async def handle_product_request(message: types.Message):
    if message.text.isdigit():
        nm_id = message.text
        response = await get_product_description(nm_id)

        if response is None:
            await message.reply(RESPONSE_ERROR)
            return
        elif response['status'] == HTTPStatus.NOT_FOUND:
            await message.reply(NOT_FOUND_ERROR)
            return
        elif response['status'] != HTTPStatus.OK:
            await message.reply(NOT_FOUND_ERROR)
            return

        product_info = get_product_info(response)

        await message.reply(product_info)
    else:
        await message.reply(NEED_CORRECT_NM_ID)


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
        logging.error(NEED_BOT_TOKEN)
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
