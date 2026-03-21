from arango import ArangoClient
import os
from dotenv import load_dotenv

load_dotenv()

ARANGO_HOST = os.getenv("ARANGO_HOST", "http://localhost:8529")
ARANGO_DB = os.getenv("ARANGO_DB")
ARANGO_USER = os.getenv("ARANGO_USER")
ARANGO_PASSWORD = os.getenv("ARANGO_PASSWORD")

client = ArangoClient(hosts=ARANGO_HOST)

db = client.db(
    ARANGO_DB,
    username=ARANGO_USER,
    password=ARANGO_PASSWORD
)

def get_db():
    return db