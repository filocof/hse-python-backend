from pydantic import BaseModel
from typing import List
from lecture_2.hw.shop_api.store.models import CartEntity

class CartItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

class CartResponse(BaseModel):
    id: int
    items: List[CartItemResponse]
    price: float

    @staticmethod
    def from_entity(entity: CartEntity) -> 'CartResponse':
        return CartResponse(
            id=entity.id,
            items=[CartItemResponse(
                id=item.id,
                name=item.name,
                quantity=item.quantity,
                available=item.available
            ) for item in entity.info.items],
            price=entity.info.price
        )