from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import json

from crud import *
from models import *

if __name__ == '__main__':
    # Base.metadata.create_all(engine)
    #
    Session = sessionmaker(bind=engine)
    s = Session()
    konfig = s.execute(select(Kofiguracija).where(Kofiguracija.api == '||||')).all()
    if len(konfig) == 0:
        print('tukss')
    print(konfig)
    # kofiguracija = Kofiguracija(
    #     api='sezona',
    #     kumulativs=True,
    #     atdalitajs='|',
    #     dati='',
    # )
    # s.add(kofiguracija)
    # s.commit()
    s.close()
