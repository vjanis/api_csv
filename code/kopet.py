import shutil
import os
import csv
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from code.logosana import logi, auditacija
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
        auditacija(darbiba='csv', parametri="Kopēt fails: " + fails + " -> " + jaunais_nosaukums,
                   autorizacijas_lvl='INFO', statuss='OK')
        os.remove(fails)
        logi(
            "Izdzēsts : " + fails + " Laiks: " + date.today().strftime("%Y%m%d") +
            '_' + datetime.datetime.now().time().strftime("%H:%M:%S"))
        auditacija(darbiba='csv', parametri="Izdzēsts fails: " + fails,
                   autorizacijas_lvl='INFO', statuss='OK')
        return jaunais_nosaukums
    except Exception as e:
        logi(
            "Kļūda kopējot: " + str(e) + " Laiks: " + date.today().strftime("%Y%m%d") +
            '_' + datetime.datetime.now().time().strftime("%H:%M:%S"))
        auditacija(darbiba='csv', parametri="Kļūda kopējot: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')
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
    Session = sessionmaker(bind=engine)
    s = Session()
    s.get(Kofiguracija, {"id": 1, "version_id": 10})
    return None


def nolasit_csv(fails, atdalitajs, kopejs_laiks):
    try:
        #konfigs = faila_konfiguracija(fails)
        with open(fails, 'r', encoding="utf-8") as file:
            csvreader = csv.reader(file, delimiter=atdalitajs)
            # saglabat_iin(csvreader, fails)
            saglabat(csvreader, fails, kopejs_laiks)
            file.close()
    except Exception as e:
        logi("Kļūda lasto failu " + str(e))
        auditacija(darbiba='csv', parametri="Kļūda lasto failu " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')



