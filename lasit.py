from datetime import datetime, date
from time import sleep
import os

import lasit
from config import *

from code import kopet_failu, nolasit_csv, logi, auditacija
from db_faili.crud import create_database

failu_mape = os.path.join('.', 'faili')
uz_mapi = os.path.join('.', 'old')
atdalitajs = CSV_ATDALITAJS
taimers = PARBAUDES_TIMERIS


def darbiba_ar_failu(fails):
    kopejs_laiks = datetime.now()
    nolasit_csv(fails, atdalitajs, kopejs_laiks)
    kopet_failu(fails, failu_mape + os.sep, uz_mapi + os.sep, kopejs_laiks)

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
        konfig = create_database()
        auditacija(darbiba='csv', parametri="Programma startējas", autorizacijas_lvl='INFO', statuss='OK')
        if konfig is not None:
            atdalitajs = konfig[0].atdalitajs
            #print(konfig[0].dati)
            taimers = int(konfig[0].dati)
        while True:
            sleep(taimers)
            #print("tagad: " + datetime.now().time().strftime("%H:%M:%S"))
            parbauda()
    except Exception as e:
        auditacija(darbiba='csv', parametri="csv beidza darbību: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK')
        logi("Draugi, nav labi! csv beidza darbību: " + str(e))
    finally:
        logi("Programma Pārtrauca darbību: " + datetime.now().time().strftime("%H:%M:%S"))
        auditacija(darbiba='csv', parametri="Programma Pārtrauca darbību", autorizacijas_lvl='INFO', statuss='OK')
