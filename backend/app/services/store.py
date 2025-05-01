from sqlalchemy.orm import Session
from ..models import Store, Inventory,Film, Rental


def get_all_stores(db: Session):
    return db.query(Store).all()


def get_films_by_store(db: Session, store_id: int):
    # Buscar todos los ítems del inventario para la tienda
    subquery = (
        db.query(Inventory)
        .filter(Inventory.store_id == store_id)
        .subquery()
    )

    # Obtener películas del inventario de la tienda que NO están actualmente alquiladas
    available_films = (
        db.query(Film)
        .join(subquery, Film.film_id == subquery.c.film_id)
        .join(Inventory, Inventory.film_id == Film.film_id)
        .outerjoin(Rental, Rental.inventory_id == Inventory.inventory_id)
        .filter(
            (Rental.return_date != None) | (Rental.rental_id == None)  # No alquiladas o ya devueltas
        )
        .distinct()
        .all()
    )

    return available_films
