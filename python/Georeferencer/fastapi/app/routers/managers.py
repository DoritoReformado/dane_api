from fastapi import HTTPException
from app.database import get_db
import logging
from arango.exceptions import CollectionCreateError
logger = logging.getLogger(__name__)

def ensure_collection(db, collection_name):
    """Asegura que la colección existe, si no la crea."""
    try:
        if not db.has_collection(collection_name):
            db.create_collection(collection_name)
            logger.info(f"Colección '{collection_name}' creada automáticamente")
    except CollectionCreateError as e:
        logger.warning(f"La colección ya existe o error al crear: {e}")
    except Exception as e:
        logger.error(f"Error asegurando colección: {e}")
        raise HTTPException(status_code=503, detail="Error de base de datos")