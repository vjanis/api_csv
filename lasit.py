from datetime import datetime, date
from time import sleep
import os

import lasit
from config import *

from code import kopet_failu, nolasit_csv, logi, auditacija, auditacijas
from db_faili.crud import create_database

failu_mape = os.path.join('.', 'faili')
uz_mapi = os.path.join('.', 'old')
atdalitajs = CSV_ATDALITAJS
taimers = PARBAUDES_TIMERIS


def darbiba_ar_failu(fails):
    kopejs_laiks = datetime.now()
    jaunais_fails = kopet_failu(fails, failu_mape + os.sep, uz_mapi + os.sep, kopejs_laiks)
    if jaunais_fails is not None:
        nolasit_csv(jaunais_fails, atdalitajs, kopejs_laiks)

def parbauda():
    for x in os.listdir(failu_mape):
        if x.endswith(".csv"):
            logi(
                "Atrasts: " + failu_mape + os.sep + x + " Laiks: " + date.today().strftime("%Y%m%d") +
                '_' +datetime.now().time().strftime("%H:%M:%S"))
            auditacijas(darbiba='fails', parametri="Atrasts: " + failu_mape + os.sep + x,
                       autorizacijas_lvl='INFO', statuss='OK', metrika=4)
            darbiba_ar_failu((failu_mape + os.sep + x))
        else:
            logi(
                "Nav korekts faila fromāts!!!: " + failu_mape + os.sep + x + " Laiks: " +
                date.today().strftime("%Y%m%d") + '_' + datetime.now().time().strftime("%H:%M:%S"))
            auditacijas(darbiba='fails', parametri="Nav korekts fails!!!: " + failu_mape + os.sep + x,
                       autorizacijas_lvl='WARN', statuss='OK', metrika=5)
        break


if __name__ == "__main__":
    try:
        konfig = create_database()
        auditacijas(darbiba='csv', parametri="Programma startējas. v"+VERSIJA, autorizacijas_lvl='INFO', statuss='OK', metrika=1)
        if konfig is not None:
            atdalitajs = konfig[0].atdalitajs
            #print(konfig[0].dati)
            taimers = int(konfig[0].dati)
        while True:
            sleep(taimers)
            #print("tagad: " + datetime.now().time().strftime("%H:%M:%S"))
            parbauda()
    except Exception as e:
        auditacijas(darbiba='csv', parametri="csv beidza darbību: " + str(e),
                   autorizacijas_lvl='ERROR', statuss='OK', metrika=3)
        logi("Draugi, nav labi! csv beidza darbību: " + str(e))
    finally:
        logi("Programma Pārtrauca darbību: " + datetime.now().time().strftime("%H:%M:%S"))
        auditacijas(darbiba='csv', parametri="Programma Pārtrauca darbību", autorizacijas_lvl='INFO',
                   statuss='OK', metrika=2)
