from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app import schemas
from arango.exceptions import CollectionCreateError
import logging
from passlib.context import CryptContext
from .managers import *


router = APIRouter(prefix="/informationtopics", tags=["informationtopics"])
logger = logging.getLogger(__name__)
collection_name = "informationtopics"

@router.get("/", response_model=list[schemas.InformationTopicBase])
def list_information_topics(db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    information_topics = [doc for doc in collection.all()]
    return information_topics

@router.post("/", response_model=schemas.InformationTopicBase)
def create_information_topic(information_topic_in: schemas.InformationTopicCreate, db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    # Comprobar si el topic existe
    existing = list(collection.find({"name": information_topic_in.name}, limit=1))
    if existing:
        raise HTTPException(status_code=400, detail="El topic ya existe")

    doc = {
        "name": information_topic_in.name,
        "description": information_topic_in.description,
    }
    meta = collection.insert(doc)
    doc["_key"] = meta["_key"]
    doc["_id"] = meta["_id"]
    return doc