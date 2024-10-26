from typing import List, Optional
from fastapi import APIRouter, HTTPException, Response
from pydantic import NonNegativeInt, PositiveInt
from http import HTTPStatus

from lecture_2.hw.shop_api.store import queries
from .contracts import ItemRequest, PatchItemRequest, ItemResponse

router = APIRouter(prefix="/item", tags=["item"])

@router.post("", status_code=HTTPStatus.CREATED)
def create_item(item: ItemRequest, response: Response) -> ItemResponse:
    entity = queries.add_item(item.as_item_info())
    response.headers["location"] = f"/item/{entity.id}"
    return ItemResponse.from_entity(entity)

@router.get("/{id}")
def get_item(id: int) -> ItemResponse:
    entity = queries.get_item(id)
    if not entity:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return ItemResponse.from_entity(entity)

@router.get("")
def list_items(
    offset: NonNegativeInt = 0,
    limit: PositiveInt = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    show_deleted: bool = False
) -> List[ItemResponse]:
    if min_price is not None and min_price < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    if max_price is not None and max_price < 0:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
        
    entities = queries.list_items(offset, limit, min_price, max_price, show_deleted)
    return [ItemResponse.from_entity(e) for e in entities]

@router.put("/{id}")
def update_item(id: int, item: ItemRequest) -> ItemResponse:
    entity = queries.update_item(id, item.as_item_info())
    if not entity:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return ItemResponse.from_entity(entity)

@router.patch("/{id}")
def patch_item(id: int, patch_data: PatchItemRequest) -> ItemResponse:
    entity = queries.patch_item(id, patch_data.as_patch_info())
    if entity is None:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED)
    return ItemResponse.from_entity(entity)

@router.delete("/{id}")
def delete_item(id: int) -> None:
    queries.delete_item(id)
    return None