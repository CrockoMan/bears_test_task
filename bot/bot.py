import asyncio
import logging
from http import HTTPStatus

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv

from constants import BOT_TOKEN
from utils import get_product_description, get_product_info

# from schemas import ProductResponse, QuantityBySize, QuantityByWh
# from utils import get_product_description


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

        # product_info = get_product_info(response.parse_raw(response['text']))
        # product = response.parse_raw(response['text'])
        # product_info = (
        #     f'Товар ID: {product.nm_id}\n'
        #     f'Цена: {product.current_price} руб.\n'
        #     f'Общий остаток: {product.sum_quantity}\n'
        #     f'Остатки по размерам:\n'
        # )
        #
        # for size in product.quantity_by_sizes:
        #     product_info += f'  Размер: {size.size}\n'
        #     for wh in size.quantity_by_wh:
        #         product_info += f'    Склад {wh.wh}: {wh.quantity} шт.\n'

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
    asyncio.run(main())
