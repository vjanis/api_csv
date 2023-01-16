import shutil
import os
import csv
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from code.logosana import logi
import json

from db_faili.crud import *
from db_faili.models import *

laiks = datetime.now();
def kopet_failu(fails, no_mapes, uz_mapi):
    jaunais_nosaukums = fails.replace(no_mapes, uz_mapi + date.today().strftime("%Y%m%d") + '_' +
                                          laiks.strftime("%H%M%S") + '_')
    shutil.copyfile(fails, jaunais_nosaukums)
    logi(
        "Pārkopēts : " + fails + " -> " + jaunais_nosaukums + " Laiks: " + date.today().strftime("%Y%m%d") +
        '_' + datetime.now().time().strftime("%H:%M:%S"))
    os.remove(fails)
    logi(
        "Izdzēsts : " + fails + " Laiks: " + date.today().strftime("%Y%m%d") +
        '_' + datetime.now().time().strftime("%H:%M:%S"))


def saglabat(csvreader, fails):
    try:
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        s = Session()
        pirma_rinda = True
        skaits = 0
        atslegas = None
        csv_faili = Csv_faili(
            api=fails[fails.rfind(os.sep)+1:fails.rfind('.')],
            csv_file_name=date.today().strftime("%Y%m%d") + '_' + laiks.strftime("%H%M%S") + '_' +
                          fails[fails.rfind(os.sep)+1:],
            created=laiks.now(),
            is_active=True
        )
        for row in csvreader:
            try:
                if pirma_rinda:
                    atslegas = row
                else:
                    #vardnica = {atslegas[i]: row[i] for i in range(len(atslegas))}
                    vardnica={}
                    csv_rinda = Csv_faili_json()
                    for atslega in atslegas:
                        for rinda in row:
                            #print(atslega + " " + rinda)
                            match str(atslega).lower():
                                case "atvk":
                                    csv_rinda.atvk = rinda
                                case "gads":
                                    csv_rinda.gads = rinda
                                case "datums":
                                    csv_rinda.datums = rinda
                            if rinda != '':
                                vardnica[atslega] = rinda
                                if rinda[0] != '0':
                                    try:
                                        vardnica[atslega] = float(str(rinda).replace(",", "."))
                                    except:
                                        pass
                                    if (str(rinda).replace(",", ".")).isdecimal() and rinda[0] != '0':
                                        vardnica[atslega] = int(rinda)
                            row.remove(rinda)
                            break
                    skaits += 1
                    print(vardnica)
                    csv_rinda.json_text = vardnica
                    csv_faili.csv_faili_json.append(csv_rinda)
            except:
                print("Problema rindā: " + row)
            finally:
                pirma_rinda = False
        s.add(csv_faili)
        s.commit()
        logi("Saglabāti ieraksti: " + str(skaits) + " fails: " + fails)

    except Exception as e:
        logi("Kļūda darbojoties ar db: " + str(e))
    finally:
        s.close()

def nolasit_csv(fails, atdalitajs):
    try:
        with open(fails, 'r', encoding="utf-8") as file:
            csvreader = csv.reader(file, delimiter=atdalitajs)
            # saglabat_iin(csvreader, fails)
            saglabat(csvreader, fails)
            file.close()
    except Exception as e:
        logi("Kļūda lasto failu " + str(e))


def saglabat_iin(csvreader, fails):
    try:
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        s = Session()
        pirma_rinda = False
        skaits = 0
        for row in csvreader:
            try:
#                print("atvk: "+row[0]+" nosaukums: "+row[1]+" gads: "+row[2]+
#                " periods: "+row[3]+" datums: "+row[4]+" sadalits: "+row[5]+" pfif: "+row[6])
                if pirma_rinda:
                    try:
                        rinda0 = str(row[0])
                    except:
                        rinda0 = ""
                    try:
                        rinda1 = str(row[1])
                    except:
                        rinda1 = ""
                    try:
                        rinda2 = str(row[2])
                    except:
                        rinda2 = ""
                    try:
                        rinda3 = str(row[3])
                    except:
                        rinda3 = ""
                    try:
                        rinda4 = str(row[4])
                    except:
                        rinda4 = ""
                    try:
                        rinda5 = float(str(row[5]).replace(",", "."))
                    except:
                        rinda5 = float("0.0")
                    try:
                        rinda6 = float(str(row[6]).replace(",", "."))
                    except:
                        rinda6 = float("0.0")
                    s.add(Book(tips='iin', atvk=rinda0, nosaukums=rinda1, gads=rinda2, periods=rinda3, datums=rinda4,
                               sadalits=rinda5,
                               pfif=rinda6
                               ))
                    skaits += 1
            except:
                print("Problema rindā: " + row)
            finally:
                pirma_rinda = True
        s.commit()
        logi("Saglabāti ieraksti: "+str(skaits) + " fails: "+fails)
    except Exception as e:
        logi("Kļūda darbojoties ar db: " + str(e))
    finally:
        s.close()

