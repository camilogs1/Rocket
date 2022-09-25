from asyncio.windows_events import NULL
from datetime import datetime


def leer_datos():
   import csv
   import pandas as pd
   # with open('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132') as csvfile:
   #    Dataset = csv.DictReader(csvfile)
   Dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI/export?format=csv')
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
   response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   credentials = json.loads(response)
   gc = gspread.service_account_from_dict(credentials)
   hoja_de_calculo = gc.open("Rocket").sheet1
   fila = hoja_de_calculo.find(carnet)
   print(fila.row, fila.col)
   hoja_de_calculo.update_cell(fila.row, fila.col+1,fecha)
   hoja_de_calculo.update_cell(fila.row, fila.col+3, hora_llegada)
   ultimaconexion = hoja_de_calculo.cell(fila.row, fila.col+2).value
   if(ultimaconexion == None):
      hoja_de_calculo.update_cell(fila.row, fila.col+2, hora_llegada)


def obtener_nombre(carnet):
   datos = leer_datos()
   for rfid, nombre in zip(datos["RFid"],datos["Nombres"]):
      if int(str(rfid)) == int(carnet):
         nombreU = nombre
   
   return nombreU

def desconexion(carnet):
   import gspread
   import requests
   import json
   import time
   from datetime import datetime
   hora_final = time.strftime("%H:%M")
   desconetado = datetime.strptime(hora_final, '%H:%M')
   response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   credentials = json.loads(response)
   gc = gspread.service_account_from_dict(credentials)
   hoja_de_calculo = gc.open("Rocket").sheet1
   fila = hoja_de_calculo.find(carnet)
   print(fila.row, fila.col)
   ultima = hoja_de_calculo.cell(fila.row, fila.col+3).value
   hora_ultima = datetime.strptime(ultima, '%H:%M:%S')
   conteo = desconetado - hora_ultima
   print(conteo)
   #tiempoinicial = hoja_de_calculo.cell(fila.row, fila.col+2).value
   #total = float(hora_final) - float(tiempoinicial)
   