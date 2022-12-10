from datetime import datetime, date
from time import sleep
import os

from code.kopet import papildu

failu_mape = r"./api_csv/faili"
uz_mapi = './api_csv/old/'
atdalitajs = '|'
taimers = 10

def darbiba_ar_failu(fails):
    papildu.nolasit_csv(fails, '|')
    papildu.kopet_failu(fails, failu_mape + '/', uz_mapi)


def parbauda():
    for x in os.listdir(failu_mape):
        if x.endswith(".csv"):
            papildu.logi(
                "Atrasts: " + failu_mape + '/' + x + " Laiks: " + date.today().strftime("%Y%m%d") + '_' +datetime.now().time().strftime("%H:%M:%S"))
            darbiba_ar_failu((failu_mape + '/' + x))
        else:
            papildu.logi(
                "Nav korekts fails!!!: " + failu_mape + '/' + x + " Laiks: " + date.today().strftime("%Y%m%d") + '_' +datetime.now().time().strftime("%H:%M:%S"))


if __name__ == "__main__":
    try:
        while True:
            sleep(taimers)
            parbauda()
    finally:
        print("BEIGAS!!! Laiks: " + datetime.now().time().strftime("%H:%M:%S"))