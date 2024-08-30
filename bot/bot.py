import asyncio
import json
import logging
import os
from urllib.parse import urlencode
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    BotCommand, BotCommandScopeDefault,
    InlineKeyboardButton, InlineKeyboardMarkup,
    WebAppInfo
)
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()
router = Router(name=__name__)
dp.include_router(router)

# Модели данных
class QuantityByWh(BaseModel):
    wh: int
    quantity: int

class QuantityBySize(BaseModel):
    size: str
    quantity_by_wh: List[QuantityByWh]

class ProductResponse(BaseModel):
    nm_id: int
    current_price: int
    sum_quantity: int
    quantity_by_sizes: List[QuantityBySize]

    class Config:
        from_attributes = True

# Пример функции для получения данных о товаре
async def get_product_info(nm_id: str) -> ProductResponse:
    # Здесь должна быть логика получения данных о товаре
    # Например, запрос к API или базе данных
    # Для примера вернем статические данные
    return ProductResponse(
        nm_id=nm_id,
        current_price=490,
        sum_quantity=10000,
        quantity_by_sizes=[
            QuantityBySize(
                size='34-36',
                quantity_by_wh=[
                    QuantityByWh(wh=3123, quantity=546),
                    QuantityByWh(wh=2331, quantity=324)
                ]
            )
        ]
    )


@router.message(CommandStart())
async def handle_start(message: types.Message):
    await message.reply('Привет! Введите nm_id товара, чтобы получить информацию.')


@router.message()
async def handle_product_request(message: types.Message):
    if message.text.isdigit():
        nm_id = message.text
        product_info = await get_product_info(nm_id)

        # Форматирование ответа
        response_text = (
            f'Товар ID: {product_info.nm_id}\n'
            f'Цена: {product_info.current_price} руб.\n'
            f'Общий остаток: {product_info.sum_quantity}\n'
            f'Остатки по размерам:\n'
        )

        for size in product_info.quantity_by_sizes:
            response_text += f'  Размер: {size.size}\n'
            for wh in size.quantity_by_wh:
                response_text += f'    Склад {wh.wh}: {wh.quantity} шт.\n'

        await message.reply(response_text)
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
