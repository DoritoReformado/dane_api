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

@router.get("/{key}", response_model=schemas.InformationTopicBase)
def get_information_topic(key: str, db = Depends(get_db)):
    """Obtener un topic por su _key"""
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    doc = collection.get(key)
    return doc

@router.put("/{key}", response_model=schemas.InformationTopicBase)
def update_information_topic_full(
    key: str, 
    information_topic_in: schemas.InformationTopicCreate, 
    db = Depends(get_db)
):
    """
    Actualización COMPLETA del topic (PUT).
    Reemplaza todos los campos del documento.
    """
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    # Verificar que existe
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    # Verificar que el nuevo nombre no esté en uso por otro documento
    if information_topic_in.name:
        existing = list(collection.find({"name": information_topic_in.name}, limit=1))
        if existing and existing[0]["_key"] != key:
            raise HTTPException(status_code=400, detail="Ya existe un topic con ese nombre")
    
    # Reemplazar el documento completo
    doc = {
        "name": information_topic_in.name,
        "description": information_topic_in.description,
        "subtopics": information_topic_in.subtopics,
    }
    
    meta = collection.update({"_key": key}, doc)
    #doc["_key"] = meta["_key"]
    doc["_id"] = meta["_id"]
    #doc["_rev"] = meta["_rev"]
    
    return doc

@router.patch("/{key}", response_model=schemas.InformationTopicBase)
def update_information_topic_partial(
    key: str, 
    information_topic_in: schemas.InformationTopicUpdate, 
    db = Depends(get_db)
):
    """
    Actualización PARCIAL del topic (PATCH).
    Solo actualiza los campos proporcionados.
    """
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    # Verificar que existe
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    # Construir documento con solo los campos enviados
    update_data = information_topic_in.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
    
    # Verificar que el nuevo nombre no esté en uso por otro documento
    if "name" in update_data:
        existing = list(collection.find({"name": update_data["name"]}, limit=1))
        if existing and existing[0]["_key"] != key:
            raise HTTPException(status_code=400, detail="Ya existe un topic con ese nombre")
    
    # Actualizar solo los campos proporcionados
    meta = collection.update({"_key": key}, update_data)
    
    # Obtener el documento actualizado completo
    updated_doc = collection.get(key)
    updated_doc = updated_doc.drop("_rev")  # Eliminar el campo _rev si no es necesario en la respuesta
    updated_doc = updated_doc.drop("_key")  # Eliminar el campo _id si no es necesario en la respuesta
    
    return updated_doc

@router.delete("/{key}", status_code=204)
def delete_information_topic(key: str, db = Depends(get_db)):
    """Eliminar un topic por su _key"""
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    
    if not collection.has(key):
        raise HTTPException(status_code=404, detail="Topic no encontrado")
    
    collection.delete(key)
    return None