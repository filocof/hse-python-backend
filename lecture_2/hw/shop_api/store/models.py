from dataclasses import dataclass
from typing import List, Optional

@dataclass(slots=True)
class ItemInfo:
    name: str
    price: float
    deleted: bool = False

@dataclass(slots=True)
class ItemEntity:
    id: int
    info: ItemInfo

@dataclass(slots=True)
class PatchItemInfo:
    name: Optional[str] = None
    price: Optional[float] = None

@dataclass(slots=True)
class CartItemInfo:
    id: int
    name: str
    quantity: int
    available: bool

@dataclass(slots=True)
class CartInfo:
    items: List[CartItemInfo] = None
    price: float = 0.0

    def __post_init__(self):
        if self.items is None:
            self.items = []

@dataclass(slots=True)
class CartEntity:
    id: int
    info: CartInfo