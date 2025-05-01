# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crear el motor de la base de datos, aquí debes poner la URL de conexión
# Dependiendo de la base de datos, cambia la URL (por ejemplo, sqlite, postgres, mysql)

DATABASE_URL = settings.DATABASE_URL  # Usamos la configuración de config.py para la URL de la base de datos

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)  # Para SQLite se agrega esta opción

# Crear la sesión que usaremos en las funciones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la clase base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()  # Establecer la conexión
    try:
        yield db  # Retornar la sesión para que pueda usarse en las rutas
    finally:
        db.close()  # Asegurarse de cerrar la sesión después de usarla
