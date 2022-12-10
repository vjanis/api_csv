import shutil
import os
import csv
from datetime import datetime, date

class papildu():
    def kopet_failu(fails, no_mapes, uz_mapi):
        jaunais_nosaukums = fails.replace(no_mapes, uz_mapi + date.today().strftime("%Y%m%d") + '_' +datetime.now().time().strftime("%H%M%S") + '_')
        shutil.copyfile(fails, jaunais_nosaukums)
        os.remove(fails)

    def nolasit_csv(fails, atdalitajs):
        with open(fails, 'r', encoding="utf-8") as file:
            csvreader = csv.reader(file, delimiter=atdalitajs)
            for row in csvreader:
                print(row)
            file.close()

    def logi(logs):
        print(logs)