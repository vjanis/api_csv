from datetime import datetime, date
from time import sleep
import os
from config import *
from code import kopet_failu, nolasit_csv, logi

failu_mape = r"./api_csv/faili"
uz_mapi = './api_csv/old/'
atdalitajs = CSV_ATDALITAJS
taimers = PARBAUDES_TIMERIS


def darbiba_ar_failu(fails):
    nolasit_csv(fails, atdalitajs)
    kopet_failu(fails, failu_mape + '/', uz_mapi)


def parbauda():
    for x in os.listdir(failu_mape):
        if x.endswith(".csv"):
            logi(
                "Atrasts: " + failu_mape + '/' + x + " Laiks: " + date.today().strftime("%Y%m%d") + '_' +datetime.now().time().strftime("%H:%M:%S"))
            darbiba_ar_failu((failu_mape + '/' + x))
        else:
            logi(
                "Nav korekts fails!!!: " + failu_mape + '/' + x + " Laiks: " + date.today().strftime("%Y%m%d") + '_' + datetime.now().time().strftime("%H:%M:%S"))


if __name__ == "__main__":
    try:
        while True:
            sleep(taimers)
            parbauda()
    finally:
        print("BEIGAS!!! Laiks: " + datetime.now().time().strftime("%H:%M:%S"))
