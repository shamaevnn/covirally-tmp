import databases
import sqlalchemy

from app.config import settings

db_options = settings.db_options

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.database_url, **db_options)
