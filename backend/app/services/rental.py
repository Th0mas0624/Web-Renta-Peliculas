from sqlalchemy.orm import Session
from ..models import Rental, Inventory, Customer, Film, Staff
from ..schemas.rental import RentalBase

from fastapi import HTTPException
from datetime import datetime

def create_rental(db: Session, rental_data: RentalBase):
    # Buscar cliente por documento (ej. email)
    customer = db.query(Customer).filter(Customer.email == rental_data.customer_email).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Verificar si hay inventario disponible (no alquilado)
    inventory = (
        db.query(Inventory)
        .filter(Inventory.film_id == rental_data.film_id)
        .filter(~Inventory.rentals.any(Rental.return_date == None))  # No esté ya alquilado
        .first()
    )
    if not inventory:
        raise HTTPException(status_code=400, detail="Película no disponible para alquilar")

    # Obtener staff de la tienda asociada
    staff = db.query(Staff).filter(Staff.store_id == inventory.store_id).first()
    if not staff:
        raise HTTPException(status_code=500, detail="No hay staff asignado en la tienda")

    # Crear objeto Rental
    new_rental = Rental(
        rental_date=rental_data.rental_date,
        inventory_id=inventory.inventory_id,
        customer_id=customer.customer_id,
        staff_id=staff.staff_id,
        return_date=None  # aún no se devuelve
    )

    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)

    return new_rental
    




