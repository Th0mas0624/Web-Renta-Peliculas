from pydantic import BaseModel
from datetime import datetime

class RentalBase(BaseModel):
    rental_date: datetime
    customer_email: str  # puede ser email, o lo adaptamos
    film_id: int

class Rental(RentalBase):
    class Config:
        from_attributes = True
    
    