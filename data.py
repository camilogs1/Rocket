def leer_datos():
   import csv
   import pandas as pd
   # with open('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132') as csvfile:
   #    Dataset = csv.DictReader(csvfile)
   Dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132')
   return Dataset

def nuevo_registro():
   import webbrowser
   import json
   webbrowser.open('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI')

def guardar_fecha(fecha, hora_llegada, carnet):
   import gspread
   import requests
   import json

   print(fecha, hora_llegada, carnet)
   # response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   # credentials = json.loads(response)
   # gc = gspread.service_account_from_dict(credentials)
   # hoja_de_calculo = gc.open("Rocket")
