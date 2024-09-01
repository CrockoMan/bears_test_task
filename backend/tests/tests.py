import pytest
from fastapi import HTTPException
from aioresponses import aioresponses

from src.constants import HTTP_PREFIX
from src.utils import (
    async_http_get, get_product_description, process_external_product_data
)


@pytest.mark.asyncio
async def test_async_http_get_success():
    url = "test-url"
    expected_response = {'status': 200, 'text': b'{"key": "value"}'}

    with aioresponses() as m:
        m.get(f"{HTTP_PREFIX}{url}", status=200, body='{"key": "value"}')

        response = await async_http_get(url)

        assert response == expected_response


@pytest.mark.asyncio
async def test_get_product_description_not_found():
    nm_id = 123

    with aioresponses() as m:
        m.get(f"{HTTP_PREFIX}{nm_id}",
              status=404)  # Simulate a not found error

        with pytest.raises(HTTPException) as exc_info:
            await get_product_description(nm_id)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == 'Item not found'


def test_process_external_product_data():
    product_data = {
        'id': 123,
        'salePriceU': 100,
        'totalQuantity': 50,
        'sizes': [
            {
                'name': 'M',
                'stocks': [{'wh': 'warehouse1', 'qty': 10},
                           {'wh': 'warehouse2', 'qty': 5}]
            },
            {
                'name': 'L',
                'stocks': [{'wh': 'warehouse1', 'qty': 20}]
            }
        ]
    }

    product = process_external_product_data(product_data)

    assert product.nm_id == 123
    assert product.current_price == 100
    assert product.sum_quantity == 50
    assert len(product.quantity_by_sizes) == 2
    assert product.quantity_by_sizes[0].size == 'M'
    assert len(product.quantity_by_sizes[0].quantity_by_wh) == 2
    assert product.quantity_by_sizes[1].size == 'L'
    assert len(product.quantity_by_sizes[1].quantity_by_wh) == 1
