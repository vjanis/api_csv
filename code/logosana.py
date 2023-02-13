

from sqlalchemy.orm import sessionmaker

from db_faili.crud import engine
from db_faili.models import Auditacija as Aa
from sqlalchemy.orm import Session
from sqlalchemy import DateTime
import datetime

def logi(logs):
    print(logs)


def auditacija(darbiba: str = '', laiks: DateTime = datetime.datetime.utcnow, parametri: str = '',
               autorizacijas_lvl: str = '', statuss: str = ''):
    try:
        audit = Aa()
        audit.darbiba = darbiba
        #audit.laiks = laiks
        audit.parametri = parametri
        audit.autorizacijas_lvl = autorizacijas_lvl
        audit.statuss = statuss
        audit.metrika = 1

        try:
            with Session(engine) as s:
                s.add(audit)
                s.commit()
        except Exception as e:
            logi("Kļūda darbojoties ar db: " + str(e))
    except Exception as e:
        logi("Kļūda piešķirot auditācijas vērtības: " + str(e))

def auditacijas(darbiba: str = '', laiks: DateTime = datetime.datetime.utcnow, parametri: str = '',
               autorizacijas_lvl: str = '', statuss: str = '', metrika: int = 0):
    try:
        audit = Aa()
        audit.darbiba = darbiba
        #audit.laiks = laiks
        audit.parametri = parametri
        audit.autorizacijas_lvl = autorizacijas_lvl
        audit.statuss = statuss
        audit.metrika = metrika

        try:
            with Session(engine) as s:
                s.add(audit)
                s.commit()
        except Exception as e:
            logi("Kļūda darbojoties ar db: " + str(e))
    except Exception as e:
        logi("Kļūda piešķirot auditācijas vērtības: " + str(e))