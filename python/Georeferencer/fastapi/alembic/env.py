import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Añadimos el path del proyecto para poder importar app.*
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import Base, DATABASE_URL
# Importar todos los modelos para que Alembic los detecte
from app import models  # ¡Esto es crucial!

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url from your DATABASE_URL
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

target_metadata = Base.metadata