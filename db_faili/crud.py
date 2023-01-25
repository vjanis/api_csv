from sqlalchemy import create_engine
from config import *
from db_faili.models import *

engine = create_engine(DATABASE_URI)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_database():
    Base.metadata.create_all(engine)
    try:
        engine.execute('CREATE INDEX dataginpathops ON csv_faili_json USING gin (json_text jsonb_path_ops);')
    except:
        pass