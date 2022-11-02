from asyncio.windows_events import NULL
from datetime import datetime, timedelta   
import gspread
import requests
import json
import numpy as np
import pandas as pd
import webbrowser
import cv2 # OpenCV para computer vision
import time
import os
import glob
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt #Para graficar

def leer_datos():
   Dataset = pd.read_csv('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI/export?format=csv')
   return Dataset

def nuevo_registro():
   webbrowser.open('https://docs.google.com/spreadsheets/d/1_4Mf30RrG7Vj43LnU8EyCZ7nb1nRrHT50J1D0zFpCzI')

def nuevo_registro_face(cedula):
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

   Ruta_dataset = 'Rostros{}'.format(cedula)
   Columnas=128
   Filas=128
   Dataset=np.zeros((4,Filas*Columnas))
   cont=0
   for i in range(0,4,1):
      Ruta=Ruta_dataset + '/rostro_' + str(i) + '_{}.jpg'.format(cedula)
      img=cv2.imread(Ruta)
      I_gris=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      I_gris=cv2.resize(I_gris, (Filas,Columnas), interpolation = cv2.INTER_AREA)
      Dataset[i,0:Filas*Columnas]=I_gris.reshape((1,Filas*Columnas))

   registrar_rostros(cedula, Dataset)

def guardar_fecha(fecha, hora_llegada, carnet):
   response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   credentials = json.loads(response)
   gc = gspread.service_account_from_dict(credentials)
   hoja_de_calculo = gc.open("Rocket").sheet1
   fila = hoja_de_calculo.find(carnet)
   hoja_de_calculo.update_cell(fila.row, fila.col+1,fecha)
   hoja_de_calculo.update_cell(fila.row, fila.col+3, hora_llegada)
   ultimaconexion = hoja_de_calculo.cell(fila.row, fila.col+2).value
   if(ultimaconexion == None):
      hoja_de_calculo.update_cell(fila.row, fila.col+2, hora_llegada)

def registrar_rostros(ID, faceid):
   faceid = pd.DataFrame(faceid)
   faceid.to_csv('bd/'+ID+'.csv')

def modelo():
   files = glob.glob('bd' + "/*.csv") 
   datos_total = []
   for i in files:
      dato = pd.read_csv(i)
      id = i.replace('bd\\','')
      id = id.replace('.csv','')
      dato['cedula'] = id
      dato = np.array(dato, dtype=int)
      for j in dato:
         datos_total.append(j)
   df = pd.DataFrame(datos_total)
   df = df.drop(0, axis=1)
   df = np.array(df)
   X = df[:,0:16384]
   Y = df[:,16384]
   X_train, X_test,Y_train, Y_test= train_test_split(X,Y,test_size=0.2,random_state=14541)
   scaler = MinMaxScaler()
   X_train = scaler.fit_transform(X_train)
   X_test = scaler.transform(X_test)
   Modelo_2 = LinearDiscriminantAnalysis()
   Modelo_2.fit(X_train, Y_train)
   
   Columnas=128
   Filas=128
   Dataset=np.zeros((1,Filas*Columnas))
   Ruta='Rostros_login/rostro.jpg'
   img=cv2.imread(Ruta)
   I_gris=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   I_gris=cv2.resize(I_gris, (Filas,Columnas), interpolation = cv2.INTER_AREA)
   Dataset=I_gris.reshape((1,Filas*Columnas))
   print(Dataset)

   Y_pred_2 =Modelo_2.predict(Dataset)
   print("Accuracy LDA",Y_pred_2)
   
   Imagen=Dataset.reshape((Filas,Columnas))
   plt.imshow(Imagen.astype('uint8'),cmap='gray',vmin=0, vmax=255)

def obtener_nombre(carnet):
   datos = leer_datos()
   for rfid, nombre in zip(datos["RFid"],datos["Nombres"]):
      if int(str(rfid)) == int(carnet):
         nombreU = nombre
   
   return nombreU

def desconexion(carnet):
   hora_final = time.strftime("%H:%M")
   desconetado = datetime.strptime(hora_final, '%H:%M')
   response = requests.get("https://drive.google.com/uc?export=download&id=1ST17tc8tq_LVmpqFn-8pcxn6Ys4S4xD9").text
   credentials = json.loads(response)
   gc = gspread.service_account_from_dict(credentials)
   hoja_de_calculo = gc.open("Rocket").sheet1
   fila = hoja_de_calculo.find(carnet)
   ultima = hoja_de_calculo.cell(fila.row, fila.col+3).value
   hora_ultima = datetime.strptime(ultima, '%H:%M')
   conteo = desconetado - hora_ultima
   total = hoja_de_calculo.cell(fila.row, fila.col+4).value
   if(total == None):
      ceros = "0:00:00"
      total = datetime.strptime(ceros, '%H:%M:%S')
   else: 
      total = datetime.strptime(total, '%H:%M:%S')

   #print(total)
   total_horas = conteo + total
   total_horas = total_horas.strftime('%H:%M:%S')
   hoja_de_calculo.update_cell(fila.row, fila.col+4, total_horas)
   