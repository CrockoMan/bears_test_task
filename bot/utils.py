import aiohttp

from constants import URL_BACKEND
from schemas import ProductResponse

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
        # raise HTTPException(status_code=404, detail='Item not found')
        return None
    return response


# async def get_product_info(nm_id: str) -> ProductResponse:
#     return await get_product_description(nm_id)
    # return ProductResponse(
    #     nm_id=nm_id,
    #     current_price=490,
    #     sum_quantity=10000,
    #     quantity_by_sizes=[
    #         QuantityBySize(
    #             size='34-36',
    #             quantity_by_wh=[
    #                 QuantityByWh(wh=3123, quantity=546),
    #                 QuantityByWh(wh=2331, quantity=324)
    #             ]
    #         )
    #     ]
    # )
