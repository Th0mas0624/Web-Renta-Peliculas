from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services.rental import create_rental
from ..schemas.rental import Rental as RentalBase
from ..models import Rental

router = APIRouter()

@router.post("/rentals/", response_model=RentalBase)
def create_new_rental(rental_data: RentalBase, db: Session = Depends(get_db)):
    return create_rental(db, rental_data)