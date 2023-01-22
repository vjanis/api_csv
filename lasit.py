from datetime import datetime, date
from time import sleep
import os
from config import *

from code import kopet_failu, nolasit_csv, logi, auditacija
from db_faili.crud import create_database

failu_mape = os.path.join('.', 'faili')
uz_mapi = os.path.join('.', 'old')
atdalitajs = CSV_ATDALITAJS
taimers = PARBAUDES_TIMERIS


def darbiba_ar_failu(fails):
    nolasit_csv(fails, atdalitajs)
    kopet_failu(fails, failu_mape + os.sep, uz_mapi + os.sep)

def parbauda():
    for x in os.listdir(failu_mape):
        if x.endswith(".csv"):
            logi(
                "Atrasts: " + failu_mape + os.sep + x + " Laiks: " + date.today().strftime("%Y%m%d") +
                '_' +datetime.now().time().strftime("%H:%M:%S"))
            auditacija(darbiba='fails', parametri="Atrasts: " + failu_mape + os.sep + x,
                       autorizacijas_lvl='INFO', statuss='OK')
            darbiba_ar_failu((failu_mape + os.sep + x))
        else:
            logi(
                "Nav korekts fails!!!: " + failu_mape + os.sep + x + " Laiks: " + date.today().strftime("%Y%m%d") +
                '_' + datetime.now().time().strftime("%H:%M:%S"))
            auditacija(darbiba='fails', parametri="Nav korekts fails!!!: " + failu_mape + os.sep + x,
                       autorizacijas_lvl='WARN', statuss='OK')


if __name__ == "__main__":
    try:
        create_database()
        auditacija(darbiba='csv', parametri="Programma startējas", autorizacijas_lvl='INFO', statuss='OK')
        while True:
            sleep(taimers)
            parbauda()
    finally:
        print("BEIGAS!!! Laiks: " + datetime.now().time().strftime("%H:%M:%S"))
        auditacija(darbiba='csv', parametri="Programma Pārtrauca darbību", autorizacijas_lvl='INFO', statuss='OK')
