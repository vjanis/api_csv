### crud.py ###

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from config import *
#from models import *

engine = create_engine(DATABASE_URI)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

