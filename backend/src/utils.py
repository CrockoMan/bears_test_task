import json
import logging
from http import HTTPStatus

import aiohttp
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.constants import HTTP_PREFIX, TIMEOUT
from src.models import Product, QuantityBySize, QuantityByWh

log = logging.getLogger(__name__)


async def async_http_get(url, timeout=TIMEOUT):

    try:
        async with (aiohttp.ClientSession() as session):
            async with session.get(
                    HTTP_PREFIX+url,
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
        log.error('Error response product id: %s', nm_id)
        raise HTTPException(status_code=404, detail='Item not found')
    return response


def process_external_product_data(product_data):
    '''Обрабатывает данные о продукте из внешнего API и сохраняет их в БД.'''
    product = Product(
        nm_id=product_data['id'],
        current_price=product_data['salePriceU'],
        sum_quantity=product_data['totalQuantity']
    )

    for size_data in product_data['sizes']:
        size = QuantityBySize(size=size_data['name'])
        size.product_id = product.nm_id

        for stock in size_data['stocks']:
            quantity_by_wh = QuantityByWh(
                wh=stock['wh'],
                quantity=stock['qty']
            )

            size.quantity_by_wh.append(quantity_by_wh)

        product.quantity_by_sizes.append(size)

    return product


# async def create_or_update_product(
#         nm_id: int,
#         db: Session,
#         update: bool = False
# ):
#
#     response = await get_product_description(str(nm_id))
#     if response is None or response['status'] != HTTPStatus.OK:
#         # log.error('Error response product id: %s', nm_id)
#         raise HTTPException(status_code=404, detail='Product not found')
#
#     data = json.loads(response['text'])
#
#     for product_data in data['data']['products']:
#         if product_data['id'] == nm_id:
#             # Проверяем, существует ли продукт в базе данных
#             existing_product = db.query(Product).filter(
#                 Product.nm_id == nm_id
#             ).first()
#
#             if not existing_product:
#                 # Создаем новый продукт
#                 log.info('Save new product: %s', nm_id)
#                 product = process_external_product_data(product_data)
#                 db.add(product)
#                 db.commit()
#                 db.refresh(product)
#                 return product
#
#             if update:
#                 # Обновляем существующий продукт
#                 log.info('Update existing product: %s', nm_id)
#                 existing_product.current_price = product_data['salePriceU']
#                 existing_product.sum_quantity = product_data['totalQuantity']
#                 existing_product.quantity_by_sizes.clear()
#
#                 for size_data in product_data['sizes']:
#                     size = QuantityBySize(size=size_data['name'])
#                     size.product_id = existing_product.nm_id
#
#                     for stock in size_data['stocks']:
#                         quantity_by_wh = QuantityByWh(
#                             wh=stock['wh'],
#                             quantity=stock['qty']
#                         )
#                         size.quantity_by_wh.append(quantity_by_wh)
#
#                     existing_product.quantity_by_sizes.append(size)
#
#                 db.commit()
#                 db.refresh(existing_product)
#                 return existing_product
#             else:
#                 return existing_product
#
#     raise HTTPException(status_code=404, detail='Product not found')
async def create_or_update_product(
        nm_id: int,
        db: Session,
        update: bool = False
):
    response = await get_product_description(str(nm_id))
    if response is None or response['status'] != HTTPStatus.OK:
        # log.error('Error response product id: %s', nm_id)
        raise HTTPException(status_code=404, detail='Product not found')

    data = json.loads(response['text'])

    for product_data in data['data']['products']:
        if product_data['id'] == nm_id:
            # Проверяем, существует ли продукт в базе данных
            existing_product = db.query(Product).filter(
                Product.nm_id == nm_id
            ).first()

            if not existing_product:
                # Создаем новый продукт
                log.info('Save new product: %s', nm_id)
                product = process_external_product_data(product_data)
                db.add(product)
                db.commit()
                db.refresh(product)
                return product

            if update:
                # Обновляем существующий продукт только в случае различия

                # Сравниваем текущие значения с новыми
                price_changed = existing_product.current_price != product_data['salePriceU']
                quantity_changed = existing_product.sum_quantity != product_data['totalQuantity']
                sizes_changed = False

                # Проверяем изменения в размерах
                existing_sizes = {size.size: size for size in existing_product.quantity_by_sizes}
                new_sizes = {size_data['name']: size_data for size_data in product_data['sizes']}

                for size_name, size_data in new_sizes.items():
                    if size_name not in existing_sizes:
                        sizes_changed = True
                        break
                    existing_size = existing_sizes[size_name]
                    # Проверяем изменения в количестве по складам
                    existing_qty_by_wh = {wh.wh: wh for wh in existing_size.quantity_by_wh}
                    for stock in size_data['stocks']:
                        if stock['wh'] not in existing_qty_by_wh or existing_qty_by_wh[stock['wh']].quantity != stock['qty']:
                            sizes_changed = True
                            break

                if price_changed or quantity_changed or sizes_changed:
                    log.info('Update existing product: %s', nm_id)
                    existing_product.current_price = product_data['salePriceU']
                    existing_product.sum_quantity = product_data['totalQuantity']
                    existing_product.quantity_by_sizes.clear()

                    for size_data in product_data['sizes']:
                        size = QuantityBySize(size=size_data['name'])
                        size.product_id = existing_product.nm_id

                        for stock in size_data['stocks']:
                            quantity_by_wh = QuantityByWh(
                                wh=stock['wh'],
                                quantity=stock['qty']
                            )
                            size.quantity_by_wh.append(quantity_by_wh)

                        existing_product.quantity_by_sizes.append(size)

                    db.commit()
                    db.refresh(existing_product)
                    return existing_product
                else:
                    return existing_product
            else:
                return existing_product

    raise HTTPException(status_code=404, detail='Product not found')
