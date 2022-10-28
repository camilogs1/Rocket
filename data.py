from asyncio.windows_events import NULL
from datetime import datetime, timedelta


def leer_datos():
   #import csv
   import pandas as pd
   # with open('https://docs.google.com/spreadsheets/d/1ypZ0E3_FNjh2LzdQiAsyraQwsCIbrXGTE9kmYVJZXwI/export?format=csv&gid=1275166132') as csvfile:
   #    Dataset = csv.DictReader(csvfile)
   Dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI/export?format=csv')
   return Dataset

def nuevo_registro():
   import webbrowser
   #import json
   webbrowser.open('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI')

def nuevo_registro_face(cedula):
   import cv2
   import os
   #Añadir la cedula al nombre de la carpeta para saber a que usuario corresponde
   if not os.path.exists('Rostros{}'.format(cedula)):
      os.makedirs('Rostros{}'.format(cedula))

   cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

   faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

   count = 0
   while count<100:
      ret,frame = cap.read()
      frame = cv2.flip(frame,1)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      auxFrame = frame.copy()

      faces = faceClassif.detectMultiScale(gray, 1.3, 5)

      k = cv2.waitKey(1)
      if k == 27:
         break

      for (x,y,w,h) in faces:
         cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
         rostro = auxFrame[y:y+h,x:x+w]
         rostro = cv2.resize(rostro,(150,150), interpolation=cv2.INTER_CUBIC)
         if count%20 == 0:
            import math
            aux = math.trunc(count/20)
            cv2.imwrite('Rostros{}/rostro_{}_{}.jpg'.format(cedula,str(aux),cedula),rostro)
            cv2.imshow('rostro',rostro)
         
         count = count +1
              
      cv2.rectangle(frame,(150,5),(450,25),(255,255,255),-1)
      cv2.putText(frame,'Acerque su rostro a la camara',(160,20), 2, 0.5,(255,0,0),1,cv2.LINE_AA)
      cv2.imshow('Rocket',frame)

   cap.release()
   cv2.destroyAllWindows()

def guardar_fecha(fecha, hora_llegada, carnet):
   import gspread
   import requests
   import json

   #print(fecha, hora_llegada, carnet)
   response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   credentials = json.loads(response)
   gc = gspread.service_account_from_dict(credentials)
   hoja_de_calculo = gc.open("Rocket").sheet1
   fila = hoja_de_calculo.find(carnet)
   #print(fila.row, fila.col)
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
   #print(fila.row, fila.col)
   ultima = hoja_de_calculo.cell(fila.row, fila.col+3).value
   hora_ultima = datetime.strptime(ultima, '%H:%M')
   conteo = desconetado - hora_ultima
   #print(conteo)
   total = hoja_de_calculo.cell(fila.row, fila.col+4).value
   if(total == None):
      ceros = "0:00:00"
      total = datetime.strptime(ceros, '%H:%M:%S')
      #total = datetime.strptime("0:00:00", "%H:%M:%S")
   else: 
      total = datetime.strptime(total, '%H:%M:%S')
      #total = total.strftime('%H:%M:%S')

   #print(total)
   total_horas = conteo + total
   #print(total_horas)
   total_horas = total_horas.strftime('%H:%M:%S')
   hoja_de_calculo.update_cell(fila.row, fila.col+4, total_horas)
   #tiempoinicial = hoja_de_calculo.cell(fila.row, fila.col+2).value
   #total = float(hora_final) - float(tiempoinicial)
   