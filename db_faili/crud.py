from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session

import code
from config import DATABASE_URI, CSV_ATDALITAJS, PARBAUDES_TIMERIS
from db_faili.models import Kofiguracija, Base, Metrikas
import time

engine = create_engine(DATABASE_URI)


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


# def create_database():
#     Base.metadata.create_all(engine)
#
#     try:
#         Session = sessionmaker(engine)
#         s = Session()
#         konfig = s.execute(select(Kofiguracija).where(Kofiguracija.api == '|||')).first()
#         if konfig is None:
#             konfig = []
#         if len(konfig) == 0:
#             kofiguracija = Kofiguracija(
#                 api='|||',
#                 kumulativs=True,
#                 atdalitajs=CSV_ATDALITAJS,
#                 dati=str(PARBAUDES_TIMERIS),
#             )
#             s.add(kofiguracija)
#             s.commit()
#             s.close()
#
#             with Session(bind=engine) as se:
#                 se.execute(text('CREATE INDEX dataginpathops ON csv_faili_json USING gin (json_text jsonb_path_ops)'))
#             se.close()
#             code.auditacija(darbiba='csv_db', parametri="Izveidota db, default konfigs un indexi",
#                             autorizacijas_lvl='INFO', statuss='OK')
#             code.logi("Izveidota db, default konfigs un indexi")
#         else:
#             return konfig
#         return None
#     except Exception as e:
#         code.auditacija(darbiba='csv_db', parametri="Draugi, nav labi! Inicējot bāzi ir kļūda:  " + str(e),
#                    autorizacijas_lvl='ERROR', statuss='OK')
#         code.logi("Draugi, nav labi! Inicējot bāzi ir kļūda: " + str(e))
#     finally:
#         s.close()


def create_database():
    Base.metadata.create_all(engine)
    try:
        with Session(engine) as se:
            konfig = se.execute(select(Kofiguracija).where(Kofiguracija.api == '|||')).first()
            if konfig is None:
                konfig = []
            if len(konfig) == 0:
                db_detalas()
    except Exception as e:
        code.auditacija(darbiba='csv_db', parametri="Draugi, nav labi! Inicējot bāzi ir kļūda:  " + str(e),
                        autorizacijas_lvl='ERROR', statuss='OK')
        code.logi("Draugi, nav labi! Inicējot bāzi ir kļūda: " + str(e))

def db_detalas():
    with Session(engine) as s:
        kofiguracija = Kofiguracija(
            api='|||',
            kumulativs=True,
            atdalitajs=CSV_ATDALITAJS,
            dati=str(PARBAUDES_TIMERIS),
        )
        s.add(kofiguracija)
        s.add(Metrikas(metrika=1, apraksts='api_csv: startējas', seciba=1))
        s.add(Metrikas(metrika=2, apraksts='api_csv: pārtrauca darbību', seciba=2))
        s.add(Metrikas(metrika=3, apraksts='api_csv: pārtrauca darbību ar kļūdu', seciba=3))
        s.add(Metrikas(metrika=4, apraksts='api_csv: Atrasts .csv fails', seciba=4))
        s.add(Metrikas(metrika=5, apraksts='api_csv: Atrasts nekortekts fails (ne .csv fails)', seciba=5))
        s.commit()
    print('1')
    with Session(engine) as s:
        s.execute(text('CREATE INDEX dataginpathops ON csv_faili_json USING gin (json_text jsonb_path_ops);'))
        s.commit()
    print('2')
    with Session(engine) as s:
        s.execute(text("CREATE OR REPLACE FUNCTION fn_metrika() RETURNS void AS "
                       "$BODY$ update metrikas set vertiba = vertiba+1 where metrika='1' $BODY$ LANGUAGE sql"))
        s.commit()
    print('3')
    with Session(engine) as s:
        s.execute(text("CREATE OR REPLACE FUNCTION tr_fn_metrika() RETURNS trigger AS $BODY$ "
                       "begin perform fn_metrika(); return new; end $BODY$ LANGUAGE plpgsql"))
        s.commit()
    print('4')
    with Session(engine) as s:
        s.execute(text("CREATE TRIGGER tr_metrika "
                       "AFTER INSERT ON auditacija FOR EACH ROW EXECUTE PROCEDURE tr_fn_metrika()"))
        s.commit()

    code.auditacija(darbiba='csv_db', parametri="Izveidota db, default konfigs un indexi",
                    autorizacijas_lvl='INFO', statuss='OK')
    code.logi("Izveidota db, default konfigs un indexi")
