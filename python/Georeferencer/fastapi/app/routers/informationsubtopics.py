from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app import schemas
from arango.exceptions import CollectionCreateError
import logging
from passlib.context import CryptContext
from .managers import *


router = APIRouter(prefix="/informationsubtopics", tags=["informationsubtopics"])
logger = logging.getLogger(__name__)
collection_name = "informationsubtopics"


@router.get("/", response_model=list[schemas.SubInformationTopicBase])
def list_information_subtopics(db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    information_subtopics = [doc for doc in collection.all()]
    return information_subtopics

@router.post("/", response_model=schemas.SubInformationTopicCreate)
def create_information_subtopic(information_subtopic_in: schemas.SubInformationTopicCreate, db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    # Comprobar si el topic existe
    existing = list(collection.find({"name": information_subtopic_in.name}, limit=1))
    if existing:
        raise HTTPException(status_code=400, detail="El topic ya existe")

    doc = {
        "name": information_subtopic_in.name,
        "description": information_subtopic_in.description,
    }
    meta = collection.insert(doc)
    doc["_key"] = meta["_key"]
    doc["_id"] = meta["_id"]
    return doc

@router.get("/{key}", response_model=schemas.SubInformationTopicBase)
def get_information_subtopic(key: str, db = Depends(get_db)):
    """Obtener un topic por su _key"""
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    doc = collection.get(key)
    return doc

@router.put("/{key}", response_model=schemas.SubInformationTopicBase)
def update_information_subtopic_full(
    key: str, 
    subinformation_topic_in: schemas.SubInformationTopicCreate, 
    db = Depends(get_db)
):
    """
    Actualización COMPLETA del topic (PUT).
    Reemplaza todos los campos del documento.
    """
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    # Verificar que el nuevo nombre no esté en uso por otro documento
    if subinformation_topic_in.name:
        existing = list(collection.find({"name": subinformation_topic_in.name}, limit=1))
        if existing and existing[0]["_key"] != key:
            raise HTTPException(status_code=400, detail="Ya existe un topic con ese nombre")

    doc = {
        "name": subinformation_topic_in.name,
        "description": information_topic_in.description,
    }
    collection.update_match({"_key": key}, doc)
    updated_doc = collection.get(key)
    return updated_doc