import shutil
import os
import csv
from datetime import datetime, date
from sqlalchemy.orm import sessionmaker
from code.logosana import logi

from db_faili.crud import *
from db_faili.models import *

class papildu():
    def kopet_failu(fails, no_mapes, uz_mapi):
        jaunais_nosaukums = fails.replace(no_mapes, uz_mapi + date.today().strftime("%Y%m%d") + '_' +
                                          datetime.now().time().strftime("%H%M%S") + '_')
        shutil.copyfile(fails, jaunais_nosaukums)
        os.remove(fails)

    def nolasit_csv(fails, atdalitajs):
        try:
            with open(fails, 'r', encoding="utf-8") as file:
                csvreader = csv.reader(file, delimiter=atdalitajs)
                saglabat_iin(csvreader, fails)
                file.close()
        except Exception as e:
            logi("Kļūda lasto failu" + str(e))


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


def iegut_tekstu(txt):
    try:
        return str(txt)
    except:
        return ""


def iegut_dalskaitli(txt):
    try:
        return float(str(txt).replace(",", "."))
    except:
        return float("0.0")

