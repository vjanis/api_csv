import shutil
import os
import csv
from datetime import datetime, date

from db_faili.crud import *
from db_faili.models import *

class papildu():
    def kopet_failu(fails, no_mapes, uz_mapi):
        jaunais_nosaukums = fails.replace(no_mapes, uz_mapi + date.today().strftime("%Y%m%d") + '_' +datetime.now().time().strftime("%H%M%S") + '_')
        shutil.copyfile(fails, jaunais_nosaukums)
        os.remove(fails)

    def nolasit_csv(fails, atdalitajs):
        try:
            with open(fails, 'r', encoding="utf-8") as file:
                csvreader = csv.reader(file, delimiter=atdalitajs)
                saglabat_iin(csvreader, fails)
                file.close()
        except Exception as e:
            print("Kļūda lasto failu" + str(e))

    def logi(logs):
        print(logs)

ef saglabat_iin(csvreader, fails):
    try:
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        s = Session()
        pirma_rinda = False
        skaits = 0
        for row in csvreader:
            try:
#                print("atvk: "+row[0]+" nosaukums: "+row[1]+" gads: "+row[2]+" periods: "+row[3]+" datums: "+row[4]+" sadalits: "+row[5]+" pfif: "+row[6])
                if pirma_rinda:
                    try:
                        rinda5 = float(str(row[5]).replace(",", "."))
                    except:
                        rinda5 = float("0.0")
                    try:
                        rinda6 = float(str(row[6]).replace(",", "."))
                    except:
                        rinda6 = float("0.0")
                    s.add(Book(tips='iin', atvk=row[0], nosaukums=row[1], gads=row[2], periods=row[3],datums=row[4],
                           sadalits=rinda5,
                               pfif=rinda6
                               ))
                    skaits += 1
            except:
                print("Problema rindā: " + row)
            finally:
                pirma_rinda = True
        s.commit()
        print("Saglabāti ieraksti: "+str(skaits)+ " fails: "+fails)
    except Exception as e:
        print("Kļūda darbojoties ar db: " + str(e))
    finally:
        s.close()
