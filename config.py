import os

password = ''
serveris = ''

ieladet_env = True

try:
    if ieladet_env:
        password = os.environ['POSTGRES_PASSWORD']
        serveris = 'api_db_image'
        del os.environ['POSTGRES_PASSWORD']
        ieladet_env = False
except:
    #Testa vide, kad nav norādīts env
    if ieladet_env:
        password = 'adminadmin'
        serveris = 'localhost'
        ieladet_env = False


DATABASE_URI = 'postgresql://postgres:'+password+'@'+serveris+':5432/postgres'

PARBAUDES_TIMERIS = 10
CSV_ATDALITAJS = '|'
