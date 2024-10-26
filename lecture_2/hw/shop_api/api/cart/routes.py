from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response
from pydantic import NonNegativeInt, PositiveInt
from http import HTTPStatus

from lecture_2.hw.shop_api.store import queries
from .contracts import CartResponse

router = APIRouter(prefix="/cart", tags=["cart"])

@router.post("", status_code=HTTPStatus.CREATED)
def create_cart(response: Response) -> CartResponse:
    entity = queries.create_cart()
    response.headers["location"] = f"/cart/{entity.id}"
    return CartResponse.from_entity(entity)

@router.get("/{id}")
def get_cart(id: int) -> CartResponse:
    entity = queries.get_cart(id)
    if not entity:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return CartResponse.from_entity(entity)

@router.get("")
def list_carts(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None
) -> List[CartResponse]:
    if min_price is not None and min_price < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    if min_quantity is not None and min_quantity < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    if max_quantity is not None and max_quantity < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)

    entities = queries.list_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)
    return [CartResponse.from_entity(e) for e in entities]

@router.post("/{cart_id}/add/{item_id}")
def add_item_to_cart(cart_id: int, item_id: int) -> CartResponse:
    entity = queries.add_item_to_cart(cart_id, item_id)
    if not entity:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return CartResponse.from_entity(entity)