from pydantic import BaseModel, ConfigDict
from typing import Optional
from lecture_2.hw.shop_api.store.models import ItemEntity, ItemInfo, PatchItemInfo

class ItemRequest(BaseModel):
    name: str
    price: float
    
    def as_item_info(self) -> ItemInfo:
        return ItemInfo(
            name=self.name,
            price=self.price
        )

class PatchItemRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    
    model_config = ConfigDict(extra="forbid")
    
    def as_patch_info(self) -> PatchItemInfo:
        return PatchItemInfo(
            name=self.name,
            price=self.price
        )

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False
    
    @staticmethod
    def from_entity(entity: ItemEntity) -> 'ItemResponse':
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
            deleted=entity.info.deleted
        )