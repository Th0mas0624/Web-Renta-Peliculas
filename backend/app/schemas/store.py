from pydantic import BaseModel
from datetime import datetime
from .address import Address

class StoreBase(BaseModel):
    address: Address
    

class Store(StoreBase):
    class Config:
        from_attributes = True
    
    