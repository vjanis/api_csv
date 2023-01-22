
from sqlalchemy.orm import sessionmaker

from db_faili.crud import *
from db_faili.models import *


def logi(logs):
    print(logs)


def auditacija(darbiba: str = '', laiks: DateTime = datetime.datetime.utcnow, parametri: str = '',
               autorizacijas_lvl: str = '', statuss: str = ''):
    try:
        audit = Auditacija()
        audit.darbiba = darbiba
        #audit.laiks = laiks
        audit.parametri = parametri
        audit.autorizacijas_lvl = autorizacijas_lvl
        audit.statuss = statuss

        try:
            Base.metadata.create_all(engine)
            session = sessionmaker(bind=engine)
            s = session()

            s.add(audit)
            s.commit()
        except Exception as e:
            logi("Kļūda darbojoties ar db: " + str(e))
        finally:
            s.close()
    except Exception as e:
        logi("Kļūda piešķirot auditācijas vērtības: " + str(e))
