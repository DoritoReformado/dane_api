from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()
# env = environ.Env()
# environ.Env.read_env()

DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_NAME = os.getenv('POSTGRES_DB')
DATABASE_HOST = os.getenv('POSTGRES_HOST', 'localhost')
DATABASE_PORT = os.getenv('POSTGRES_PORT', '5432')

DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener sesión en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()