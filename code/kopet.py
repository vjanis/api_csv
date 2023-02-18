import shutil
import os
import csv
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import select
from code.logosana import logi, auditacija, auditacijas
import json

from db_faili.crud import *
from db_faili.models import *

def kopet_failu(fails, no_mapes, uz_mapi, kopejs_laiks):
    try:
        laiks = kopejs_laiks
        jaunais_nosaukums = fails.replace(no_mapes, uz_mapi + laiks.strftime('%Y%m%d_%H%M%S%f')[:-3] + '_')
        shutil.copyfile(fails, jaunais_nosaukums)
        logi(
            "Pārkopēts : " + fails + " -> " + jaunais_nosaukums + " Laiks: " + date.today().strftime("%Y%m%d") +
            '_' + datetime.datetime.now().time().strftime("%H:%M:%S"))
        auditacijas(darbiba='csv_api', parametri="Kopēt fails: " + fails + " -> " + jaunais_nosaukums,
                   autorizacijas_lvl='INFO', statuss='OK', metrika=14)
        os.remove(fails)
        logi(
            "Izdzēsts : " + fails + " Laiks: " + date.today().strftime("%Y%m%d") +
            '_' + datetime.datetime.now().time().strftime("%H:%M:%S"))
        auditacijas(darbiba='csv_api', parametri="Izdzēsts fails: " + fails,
                   autorizacijas_lvl='INFO', statuss='OK', metrika=15)
        return jaunais_nosaukums
    except Exception as e:
        logi(
            "Kļūda kopējot: " + str(e) + " Laiks: " + date.today().strftime("%Y%m%d") +
            '_' + datetime.datetime.now().time().strftime("%H:%M:%S"))
        auditacijas(darbiba='csv_api', parametri="Kļūda kopējot: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK', metrika=16)
        return None


def saglabat(csvreader, fails, kopejs_laiks):
    try:
        laiks = kopejs_laiks
        #Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        s = Session()
        pirma_rinda = True
        skaits = 0
        atslegas = None
        csv_faili = Csv_faili(
            api=str(fails[fails.rfind(os.sep)+1:fails.rfind('.')])[38:],
            csv_file_name=fails[fails.rfind(os.sep)+1:],
            # created=laiks.now(),
            is_active=True
        )
        for row in csvreader:
            try:
                if pirma_rinda:
                    atslegas = row
                else:
                    vardnica={}
                    csv_rinda = Csv_faili_json()
                    for atslega in atslegas:
                        for rinda in row:
                            if rinda != '':
                                if rinda[0] != '0':
                                    if rinda.isdecimal():
                                        vardnica[atslega] = int(rinda)
                                    else:
                                        try:
                                            vardnica[atslega] = float(str(rinda).replace(",", "."))
                                        except:
                                            vardnica[atslega] = rinda
                                else:
                                    vardnica[atslega] = rinda
                            row.remove(rinda)
                            break
                    skaits += 1
                    csv_rinda.json_text = vardnica
                    csv_faili.csv_faili_json.append(csv_rinda)
            except:
                print("Problema rindā: " + row)
                auditacija(darbiba='csv', parametri="Problema rindā: " + row,
                           autorizacijas_lvl='ERROR', statuss='OK')
            finally:
                pirma_rinda = False
        s.add(csv_faili)
        s.commit()
        auditacija(darbiba='csv', parametri="Saglabāti ieraksti: " + str(skaits) + " fails: " + fails,
                   autorizacijas_lvl='INFO', statuss='OK')
        logi("Saglabāti ieraksti: " + str(skaits) + " fails: " + fails)

    except Exception as e:
        logi("Kļūda darbojoties ar db: " + str(e))
        auditacija(darbiba='csv', parametri="Kļūda darbojoties ar db: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')
    finally:
        s.close()


def faila_konfiguracija(fails):
    with Session(engine) as session:
        statement = select(Kofiguracija).filter_by(api=str(fails[fails.rfind(os.sep)+1:fails.rfind('.')])[38:],
                                                   statuss=True)
        conf_obj = session.scalars(statement).all()
    #session.close()

    return conf_obj


def nolasit_csvO(fails, atdalitajs, kopejs_laiks):
    try:
        konfigs = faila_konfiguracija(fails)
        print(konfigs)

        with open(fails, 'r', encoding="utf-8") as file:
            csvreader = csv.reader(file, delimiter=atdalitajs)
            # saglabat_iin(csvreader, fails)
            saglabat(csvreader, fails, kopejs_laiks)
            file.close()
    except Exception as e:
        logi("Kļūda lasto failu: " + str(e))
        auditacija(darbiba='csv', parametri="Kļūda lasto failu: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')

def nolasit_csv(fails, atdalitajs, kopejs_laiks):
    kumulativs = True
    try:
        konfigs = faila_konfiguracija(fails)
        #print(konfigs)
        skaits = 0
        csv_faili = Csv_faili(
            api=str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:],
            csv_file_name=fails[fails.rfind(os.sep) + 1:],
            is_active=True
        )
        ir_configs = False
        if konfigs is not None:
            if len(konfigs) != 0:
                conf = konfigs[0].json_text
                atdalitajs = konfigs[0].atdalitajs
                kumulativs = konfigs[0].kumulativs
                ir_configs = True
        with open(fails, 'r', encoding="utf-8") as file:
            first_line = file.readline()
            file.seek(0)
            csvreader = csv.DictReader(file, delimiter=atdalitajs)
            for row in csvreader:
                skaits += 1
                if ir_configs:
                    for key, value in conf.items():
                        #print(key, value)
                        match value:
                            # Noklusēti visi ir String
                            # case 'String':
                            #     print(key + " (String): " + row[key])
                            case 'Integer':
                                kluda = False
                                try:
                                    row[key] = int(row[key])
                                    # print(key + " (Integer): " + str(row[key]))
                                    # print(type(row))
                                except Exception as e:
                                    kluda = True
                                    auditacijas(darbiba='api_csv', parametri="fails neatbilst konfigurācijai api: "
                                                                             + str(
                                        fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                                                             + " fails: " + fails,
                                                autorizacijas_lvl='ERROR', statuss='OK', metrika=11)
                                    logi("fails neatbilst konfigurācijai api: " + str(
                                        fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                         + " fails: " + fails + " rinda(Integer): " + str(skaits)
                                         + " Vertibas: {" + key + ": " + str(row[key]) + "}")
                                if kluda:
                                    if key in row:
                                        del row[key]
                            case 'Float':
                                kluda = False
                                try:
                                    row[key] = float(row[key].replace(",", "."))
                                    # print(key + " (Float): " + str(row[key]))
                                except Exception as e:
                                    kluda = True
                                    auditacijas(darbiba='api_csv', parametri="fails neatbilst konfigurācijai api: "
                                                                             + str(
                                        fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                                                             + " fails: " + fails,
                                                autorizacijas_lvl='ERROR', statuss='OK', metrika=11)
                                    logi("fails neatbilst konfigurācijai api: " + str(
                                        fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                         + " fails: " + fails + " rinda(Float): " + str(skaits)
                                         + " Vertibas: {" + key + ": " + str(row[key]) + "}")
                                if kluda:
                                    if key in row:
                                        del row[key]

                csv_rinda = Csv_faili_json()
                csv_rinda.json_text = row
                csv_faili.csv_faili_json.append(csv_rinda)

        if not ir_configs:
            konf = first_line.replace('\n', '').split(atdalitajs)
            vard = dict.fromkeys(konf, "String")
            kofiguracija = Kofiguracija()
            kofiguracija.api = str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
            kofiguracija.kumulativs = True
            kofiguracija.atdalitajs = atdalitajs
            kofiguracija.json_text = vard
            with Session(engine) as s:
                s.add(kofiguracija)
                s.commit()
            auditacijas(darbiba='api_csv', parametri="Saglabata faila konfigurācija. api: "
                                                     + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                                     + " fails: " + fails,
                       autorizacijas_lvl='INFO', statuss='OK', metrika=10)
            logi("Saglabata faila konfigurācija. api: " + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                 + " fails: " + fails)

        with Session(engine) as s:
            if not kumulativs:
                s.query(Csv_faili).filter(Csv_faili.api == str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]). \
                    update({'is_active': False})
            s.add(csv_faili)
            s.commit()
        auditacijas(darbiba='api_csv', parametri="Saglabats fails. api: "
                                                 + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                                 + " Ieraksti: " + str(skaits)
                                                 + " fails: " + fails,
                    autorizacijas_lvl='INFO', statuss='OK', metrika=12)
        logi("Saglabats fails. api: " + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
             + " Ieraksti: " + str(skaits) + " fails: " + fails)

    except Exception as e:
        auditacijas(darbiba='api_csv', parametri="Saglabājot failu radās kļūda. api: "
                                                 + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
                                                 + " fails: " + fails,
                    autorizacijas_lvl='ERROR', statuss='OK', metrika=13)
        logi("Saglabājot failu radās kļūda. api: " + str(fails[fails.rfind(os.sep) + 1:fails.rfind('.')])[38:]
             + " fails: " + fails + " kļūda: " + str(e))


