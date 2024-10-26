from typing import Dict, List, Optional, Iterable
from .models import ItemInfo, ItemEntity, CartInfo, CartEntity, CartItemInfo, PatchItemInfo

_items: Dict[int, ItemInfo] = {}
_carts: Dict[int, CartInfo] = {}
_last_item_id = 0
_last_cart_id = 0

def add_item(info: ItemInfo) -> ItemEntity:
    global _last_item_id
    _last_item_id += 1
    _items[_last_item_id] = info
    return ItemEntity(id=_last_item_id, info=info)

def get_item(id: int) -> Optional[ItemEntity]:
    if id not in _items or _items[id].deleted:
        return None
    return ItemEntity(id=id, info=_items[id])

def list_items(offset: int = 0, limit: int = 10, 
               min_price: Optional[float] = None,
               max_price: Optional[float] = None,
               show_deleted: bool = False) -> List[ItemEntity]:
    result = []
    for id, info in _items.items():
        if not show_deleted and info.deleted:
            continue
        if min_price is not None and info.price < min_price:
            continue
        if max_price is not None and info.price > max_price:
            continue
        result.append(ItemEntity(id=id, info=info))
    return result[offset:offset + limit]

def update_item(id: int, info: ItemInfo) -> Optional[ItemEntity]:
    if id not in _items or _items[id].deleted:
        return None
    _items[id] = info
    return ItemEntity(id=id, info=info)

def patch_item(id: int, patch_info: PatchItemInfo) -> Optional[ItemEntity]:
    if id not in _items:
        return None
    
    current_info = _items[id]
    if current_info.deleted:
        return None
        
    if patch_info.name is not None:
        current_info.name = patch_info.name
    if patch_info.price is not None:
        current_info.price = patch_info.price
        
    return ItemEntity(id=id, info=current_info)

def delete_item(id: int) -> None:
    if id in _items:
        _items[id].deleted = True
    return None

def create_cart() -> CartEntity:
    global _last_cart_id
    _last_cart_id += 1
    cart_info = CartInfo()
    _carts[_last_cart_id] = cart_info
    return CartEntity(id=_last_cart_id, info=cart_info)

def get_cart(id: int) -> Optional[CartEntity]:
    if id not in _carts:
        return None
    return CartEntity(id=id, info=_carts[id])

def list_carts(offset: int = 0, limit: int = 10,
               min_price: Optional[float] = None,
               max_price: Optional[float] = None,
               min_quantity: Optional[int] = None,
               max_quantity: Optional[int] = None) -> List[CartEntity]:
    result = []
    for id, info in _carts.items():
        total_quantity = sum(item.quantity for item in info.items)
        if min_price is not None and info.price < min_price:
            continue
        if max_price is not None and info.price > max_price:
            continue
        if min_quantity is not None and total_quantity < min_quantity:
            continue
        if max_quantity is not None and total_quantity > max_quantity:
            continue
        result.append(CartEntity(id=id, info=info))
    return result[offset:offset + limit]

def add_item_to_cart(cart_id: int, item_id: int) -> Optional[CartEntity]:
    if cart_id not in _carts or item_id not in _items:
        return None
        
    cart_info = _carts[cart_id]
    item_info = _items[item_id]
    
    for cart_item in cart_info.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            cart_info.price += item_info.price
            return CartEntity(id=cart_id, info=cart_info)
    
    cart_info.items.append(CartItemInfo(
        id=item_id,
        name=item_info.name,
        quantity=1,
        available=not item_info.deleted
    ))
    cart_info.price += item_info.price
    return CartEntity(id=cart_id, info=cart_info)