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
                    s.add(Book(tips='iin', atvk=iegut_tekstu(row[0]), nosaukums=iegut_tekstu(row[1]),
                               gads=iegut_tekstu(row[2]), periods=iegut_tekstu(row[3]), datums=iegut_tekstu(row[4]),
                               sadalits=iegut_dalskaitli(row[5]), pfif=iegut_dalskaitli(row[6])
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

