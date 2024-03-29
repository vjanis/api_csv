from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

import code
from config import DATABASE_URI, CSV_ATDALITAJS, PARBAUDES_TIMERIS, VERSIJA
from db_faili.models import Kofiguracija, Base, Metrikas

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
                db_detalas()
            else:
                db_versija(konfig[0].json_text['versija'])
            # if len(konfig) == 0:
            #     db_detalas()
    except Exception as e:
        code.auditacijas(darbiba='api_csv', parametri="Draugi, nav labi! Inicējot bāzi ir kļūda:  " + str(e),
                        autorizacijas_lvl='ERROR', statuss='OK', metrika=3)
        code.logi("Draugi, nav labi! Inicējot bāzi ir kļūda: " + str(e))

def db_versija(kofig):
    try:
        db_versija = int(str(kofig[1:]).replace(".", ""))
        #app_versija = int(str(VERSIJA[1:]).replace(".", ""))

        # v01.00.01
        if db_versija < 10001:
            with Session(engine) as s:
                s.add(Metrikas(metrika=21, param='api_local_web_info',
                               apraksts='api_local_web: INFO', seciba=21))
                s.add(Metrikas(metrika=22, param='api_local_web_info_error',
                               apraksts='api_local_web: INFO ERROR', seciba=22))
                s.add(Metrikas(metrika=23, param='api_local_web_auditacija',
                               apraksts='api_local_web: auditacija', seciba=23))
                s.add(Metrikas(metrika=24, param='api_local_web_auditacija_error',
                               apraksts='api_local_web: auditacija ERROR', seciba=24))
                s.add(Metrikas(metrika=25, param='api_csv_versija',
                               apraksts='api_csv: izpilditi versijas skripti', seciba=25))
                s.add(Metrikas(metrika=26, param='api_csv_versija',
                               apraksts='api_csv: izpilditi versijas skripti ERROR', seciba=26))

                s.query(Kofiguracija).filter(Kofiguracija.api == '|||')\
                    .update({Kofiguracija.json_text: {"versija": VERSIJA}}, synchronize_session=False)
                s.commit()
                code.auditacijas(darbiba='api_csv',
                                 parametri="Izpilditi versijas skripts: v01.00.01 ceļot no " + kofig + " uz versiju: "
                                           + VERSIJA,
                                 autorizacijas_lvl='INFO', statuss='OK', metrika=25)
                code.logi("Izpilditi versijas skripts:  v01.00.01 ceļot uz versiju: " + VERSIJA)

        # v01.00.02
        if db_versija < 10002:
            with Session(engine) as s:
                s.add(Metrikas(metrika=27, param='api_faili_web_authentifikacija_error',
                               apraksts='api_faili_web: Nekorekts lietotājvārds vai parole', seciba=27))
                s.query(Kofiguracija).filter(Kofiguracija.api == '|||')\
                    .update({Kofiguracija.json_text: {"versija": VERSIJA}}, synchronize_session=False)
                s.commit()
                code.auditacijas(darbiba='api_csv',
                                 parametri="Izpilditi versijas skripts: v01.00.02 ceļot no " + kofig + " uz versiju: "
                                           + VERSIJA,
                                 autorizacijas_lvl='INFO', statuss='OK', metrika=25)
                code.logi("Izpilditi versijas skripts:  v01.00.02 ceļot uz versiju: " + VERSIJA)

            # v01.00.03
            if db_versija < 10003:
                with Session(engine) as s:
                    s.add(Metrikas(metrika=28, param='api_web_api_config_error',
                                   apraksts='api_web: nav api konfigurācijas pieprasot API datu', seciba=28))
                    s.add(Metrikas(metrika=29, param='api_web_api_filter_error',
                                   apraksts='api_web: nekorekti filtra parametri', seciba=29))
                    s.query(Kofiguracija).filter(Kofiguracija.api == '|||') \
                        .update({Kofiguracija.json_text: {"versija": VERSIJA}}, synchronize_session=False)
                    s.commit()
                    code.auditacijas(darbiba='api_csv',
                                     parametri="Izpilditi versijas skripts: v01.00.03 ceļot no " + kofig + " uz versiju: "
                                               + VERSIJA,
                                     autorizacijas_lvl='INFO', statuss='OK', metrika=25)
                    code.logi("Izpilditi versijas skripts:  v01.00.03 ceļot uz versiju: " + VERSIJA)

    except Exception as e:
        code.auditacijas(darbiba='api_csv', parametri="Pildot versijas skriptus kļūda:  " + VERSIJA + " err:" + str(e),
                         autorizacijas_lvl='ERROR', statuss='OK', metrika=26)
        code.logi("Versijas skriptos kļūda: " + VERSIJA + " err:" + str(e))


def db_detalas():
    with Session(engine) as s:
        kofiguracija = Kofiguracija(
            api='|||',
            kumulativs=True,
            json_text={"versija": VERSIJA},
            atdalitajs=CSV_ATDALITAJS,
            dati=str(PARBAUDES_TIMERIS),
        )
        s.add(kofiguracija)
        s.add(Metrikas(metrika=1, param='api_csv_start', apraksts='api_csv: startējas', seciba=1))
        s.add(Metrikas(metrika=2, param='api_csv_stop', apraksts='api_csv: pārtrauca darbību', seciba=2))
        s.add(Metrikas(metrika=3, param='api_csv_error', apraksts='api_csv: pārtrauca darbību ar kļūdu', seciba=3))
        s.add(Metrikas(metrika=4, param='api_csv_find_csv_file', apraksts='api_csv: Atrasts .csv fails', seciba=4))
        s.add(Metrikas(metrika=5, param='api_csv_find_incorrect_file',
                       apraksts='api_csv: Atrasts nekortekts fails (ne .csv fails)', seciba=5))
        s.add(Metrikas(metrika=6, param='api_faili_web_file_too_large',
                       apraksts='api_faili_web: Augšuplādēts fails par lielu', seciba=6))
        s.add(Metrikas(metrika=7, param='api_faili_web_incorrect_file',
                       apraksts='api_faili_web: Augšuplādēts nekortekts fails (ne .csv fails)', seciba=7))
        s.add(Metrikas(metrika=8, param='api_faili_web_csv_file_upload',
                       apraksts='api_faili_web: Augšuplādēts .csv fails', seciba=8))
        s.add(Metrikas(metrika=9, param='api_faili_web_error', apraksts='api_faili_web: Augšuplāde kļūdaina', seciba=9))
        s.add(Metrikas(metrika=10, param='api_csv_save_config',
                       apraksts='api_csv: Saglabata faila konfigurācija', seciba=10))
        s.add(Metrikas(metrika=11, param='api_csv_save_faile_config_error',
                       apraksts='api_csv: Saglabājot failu, fails neatbilst konfigurācijai', seciba=11))
        s.add(Metrikas(metrika=12, param='api_csv_save_faile',
                       apraksts='api_csv: Saglabāti faili', seciba=12))
        s.add(Metrikas(metrika=13, param='api_csv_save_faile_error',
                       apraksts='api_csv: Saglabājot failu radusies kļūda', seciba=13))
        s.add(Metrikas(metrika=14, param='api_csv_copy_faile',
                       apraksts='api_csv: Pārkopēts fails no mapes kur tiek augšuplādēts uz arhīva mapi', seciba=14))
        s.add(Metrikas(metrika=15, param='api_csv_delete_faile',
                       apraksts='api_csv: Izdzēsts fails no augšuplādes mapes', seciba=15))
        s.add(Metrikas(metrika=16, param='api_csv_delete_copy_faile_error',
                       apraksts='api_csv: kopējot vai dzēšot failu notikusi kļūda', seciba=16))
        s.add(Metrikas(metrika=17, param='api_csv_create_db_config_index',
                       apraksts='api_csv: Izveidota datubāze, konfigurācija, index, trigeri, fnkcijas', seciba=17))
        s.add(Metrikas(metrika=18, param='api_csv_create_db_config_index_error',
                       apraksts='api_csv: kļūda veidojot sākotnējo datubāzi', seciba=18))
        s.add(Metrikas(metrika=19, param='api_web_atvertie_dati',
                       apraksts='api_web: pieprasījumi uz atvērtajiem datiem', seciba=19))
        s.add(Metrikas(metrika=20, param='api_web_atvertie_dati_error',
                       apraksts='api_web: kļūdas veidojot atvērto datu pieprasījumu', seciba=20))
        s.commit()

    with Session(engine) as s:
        s.execute(text('CREATE INDEX dataginpathops ON csv_faili_json USING gin (json_text jsonb_path_ops);'))
        s.commit()
    with Session(engine) as s:
        s.execute(text("CREATE OR REPLACE FUNCTION fn_metrika(metrik int) RETURNS void AS "
                       "$BODY$ update metrikas set vertiba = vertiba+1 where metrika=metrik $BODY$ LANGUAGE sql"))
        s.commit()
    with Session(engine) as s:
        s.execute(text("CREATE OR REPLACE FUNCTION tr_fn_metrika() RETURNS trigger AS $BODY$ "
                       "begin perform fn_metrika(NEW.metrika); return new; end $BODY$ LANGUAGE plpgsql"))
        s.commit()
    with Session(engine) as s:
        s.execute(text("CREATE TRIGGER tr_metrika "
                       "AFTER INSERT ON auditacija FOR EACH ROW EXECUTE PROCEDURE tr_fn_metrika()"))
        s.commit()
    db_versija('v00.00.00')
    code.auditacijas(darbiba='api_csv', parametri="Izveidota db, default konfigs, funkcijas, trigeri un indexi",
                    autorizacijas_lvl='INFO', statuss='OK')
    code.logi("Izveidota db: " + VERSIJA + ", default konfigs, funkcijas, trigeri un indexi")
