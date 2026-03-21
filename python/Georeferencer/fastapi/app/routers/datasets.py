from fastapi import APIRouter, Depends, UploadFile, File
from app.database import get_db
from pathlib import Path
from datetime import datetime
import shutil
from .managers import *

collection_name = "datasets"
router = APIRouter()

BASE_MEDIA = Path("app/media")

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/")
def list_datasets(db = Depends(get_db)):
    ensure_collection(db, collection_name)
    collection = db.collection(collection_name)
    datasets = [doc for doc in collection.all()]
    return datasets


@router.post("/upload")
async def upload_dataset(
    topic: str,
    subtopic: str,
    dataset: str,
    file: UploadFile = File(...)
):

    # fecha
    fecha = datetime.now().strftime("%Y_%m_%d")

    # extension
    ext = file.filename.split(".")[-1]

    filename = f"{dataset}_{fecha}.{ext}"

    folder = BASE_MEDIA / topic / subtopic / dataset

    folder.mkdir(parents=True, exist_ok=True)

    filepath = folder / filename

    with filepath.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    source_ref = f"/media/{topic}/{subtopic}/{dataset}/{filename}"

    return {
        "message": "dataset uploaded",
        "source_ref": source_ref
    }