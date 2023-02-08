from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker

import code
from config import DATABASE_URI, CSV_ATDALITAJS, PARBAUDES_TIMERIS
from db_faili.models import Kofiguracija, Base

engine = create_engine(DATABASE_URI)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def create_database():
    Base.metadata.create_all(engine)
    try:
        Session = sessionmaker(engine)
        s = Session()
        konfig = s.execute(select(Kofiguracija).where(Kofiguracija.api == '|||')).first()
        if konfig is None:
            konfig = []
        if len(konfig) == 0:
            kofiguracija = Kofiguracija(
                api='|||',
                kumulativs=True,
                atdalitajs=CSV_ATDALITAJS,
                dati=str(PARBAUDES_TIMERIS),
            )
            s.add(kofiguracija)
            s.commit()
            s.close()

            with Session(bind=engine) as se:
                se.execute(text('CREATE INDEX dataginpathops ON csv_faili_json USING gin (json_text jsonb_path_ops)'))
            se.close()
            code.auditacija(darbiba='csv_db', parametri="Izveidota db, default konfigs un indexi",
                            autorizacijas_lvl='INFO', statuss='OK')
            code.logi("Izveidota db, default konfigs un indexi")
        else:
            return konfig
        return None
    except Exception as e:
        code.auditacija(darbiba='csv_db', parametri="Draugi, nav labi! Inicējot bāzi ir kļūda:  " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')
        code.logi("Draugi, nav labi! Inicējot bāzi ir kļūda: " + str(e))
    finally:
        s.close()
