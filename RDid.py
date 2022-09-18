import pandas as pd

#Cargando datos del dataset
dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132')

tagId=str(input('Acerque su carnet al lector: '))

import getpass
import csv
tagId = getpass.getpass("Acerque su carnet al lector: ")
RFidRegistered = False
with open('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132') as csvfile:
     Dataset = csv.DictReader(csvfile)
     for idx in Dataset:
        if str(idx["RFid"]) == tagId:
           RFidRegistered = True
           print("Bienvenido " + idx["Nombres"])
     if RFidRegistered == False:
        print("No se ha encontrado el usuario")