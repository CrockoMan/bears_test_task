import json

import aiohttp

from schemas import ProductResponse
from constants import URL_BACKEND

TIMEOUT = 2


async def async_http_get(url, timeout=TIMEOUT):

    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(
                    URL_BACKEND + 'products/' + url,
                    timeout=timeout
            ) as response:
                text = await response.read()
        return {
            'status': response.status,
            'text': text
        }
    except Exception as e:
        return None


async def get_product_description(nm_id):
    response = await async_http_get(nm_id)
    if not response:
        return None
    return response


def get_product_info(product_obj):
    json_data = json.loads(product_obj['text'])

    product = ProductResponse(**json_data)
    product_info = (
        f'Товар ID: {product.nm_id}\n'
        f'Цена: {product.current_price // 100}.'
        f'{(product.current_price % 100):02} руб.\n'
        f'Общий остаток: {product.sum_quantity}\n'
        f'Остатки:\n'
    )

    for size in product.quantity_by_sizes:
        for wh in size.quantity_by_wh:
            product_info += f'    Склад {wh.wh}:  {wh.quantity} \n'

    return product_info
