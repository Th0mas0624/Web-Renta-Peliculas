import os

class Settings:
    PROJECT_NAME: str = "My FastAPI App"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://admin:Migue.0416@sakila.crga0ie0wgfc.us-east-1.rds.amazonaws.com:3306/sakila")

settings = Settings()