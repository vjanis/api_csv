from datetime import datetime
from sqlalchemy.orm import sessionmaker
import json

from crud import *
from models import *

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    s = Session()
    # some JSON:
    x = '{ "name":"John", "age":30, "city":"New York"}'

    # parse x:
    y = json.loads(x)
    # convert into JSON:
    z = json.dumps(x)
    csv_faili = Csv_faili(

        api='iin',
        csv_file_name='faila_nosaukums',
        created=datetime.now(),
        is_active=True
    )
    csv_faili.csv_faili_json = [

        Csv_faili_json(atvk='001100', json_text=y),
        Csv_faili_json(json_text=z)
    ]
    s.add(csv_faili)
    s.commit()
    s.close()
