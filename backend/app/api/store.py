from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..services.store import get_all_stores, get_films_by_store
from ..schemas.store import Store
from ..schemas.film import FilmBase

router = APIRouter()

@router.get("/stores/", response_model=List[Store])
def list_stores(db: Session = Depends(get_db)):
    return get_all_stores(db)

@router.get("/stores/{store_id}/films", response_model=List[FilmBase])
def list_films_by_store(store_id: int, db: Session = Depends(get_db)):
    films = get_films_by_store(db, store_id)
    if not films:
        raise HTTPException(status_code=404, detail="No hay películas disponibles en esta tienda.")
    return films
