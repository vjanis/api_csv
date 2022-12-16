### crud.py ###

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_faili.config import *
from db_faili.models import *

engine = create_engine(DATABASE_URI)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

