from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app import schemas
from arango.exceptions import CollectionCreateError
import logging
from passlib.context import CryptContext
from .managers import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

collection_name = "users"
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/", response_model=list[schemas.User])
def list_users(db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    users = [doc for doc in collection.all()]
    return users

@router.post("/", response_model=schemas.User)
def create_user(user_in: schemas.UserCreate, db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    # Comprobar si email existe
    existing = list(collection.find({"email": user_in.email}, limit=1))
    if existing:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    hashed_password = get_password_hash(user_in.password)

    doc = {
        "email": user_in.email,
        "full_name": user_in.full_name,
        "hashed_password": hashed_password,  # aquí deberías hashearla
    }
    meta = collection.insert(doc)
    doc["_key"] = meta["_key"]
    return doc