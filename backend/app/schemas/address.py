from pydantic import BaseModel
from datetime import datetime

class AddressBase(BaseModel):
    address: str
    district: str  # puede ser email, o lo adaptamos
    
class Address(AddressBase):
    class Config:
        from_attributes = True
    
    