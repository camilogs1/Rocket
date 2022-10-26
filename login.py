from tkinter import *
import os
import tkinter
import tkinter.font as tkFont
from cliente import cliente
from data import *
import time
from datetime import datetime
import cv2
pestas_color='#dd5228'

# Ventana de inicio
def ventana_inicio():
    global ventana_principal
    ventana_principal=Tk()
    ventana_principal.geometry("300x250")#Dimension
    ventana_principal.title("Rocket")#Titulo
    ventana_principal.iconbitmap('data/zorro.ico')

    Label (text="Bienvenido a Rocket", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (text="").pack()
    Button(text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color, command=login,
    foreground = "white", activeforeground = '#dd5228').pack()
    Label (text="").pack()
    #Imagen
    rocket = PhotoImage(file='data/zorro.png').subsample(4,4)
    Label(ventana_principal, image=rocket).pack()

    ventana_principal.mainloop()

# Ventana acceder/Login
def login ():
    global ventana_login
    ventana_login = Toplevel()
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry ("330x250")
    ventana_login.iconbitmap('data/zorro.ico')

    Label (ventana_login, text="Acerque su carnet por el lector", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (ventana_login, text="") .pack()

    global verifica_usuario
    verifica_usuario = StringVar()
    global entrada_login_usuario

    entrada_login_usuario = Entry(ventana_login, textvariable = verifica_usuario)
    entrada_login_usuario.focus()
    entrada_login_usuario.pack()
    entrada_login_usuario.bind("<Return>", verifica_login)

    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), command = verifica_login,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228').pack()
    Label(ventana_login, text="").pack()
    #Gif
    rocket = PhotoImage(file='data/origamiRFid Negro.png').subsample(4,4)
    Label(ventana_login, image=rocket).place(x=70,y=30)
    #Acceso ventana FACEID
    rocket_FACEID = PhotoImage(file='data/abstractoFACEid.png').subsample(9,9)
    Button(ventana_login, image=rocket_FACEID, command = ventana_FACEID).place(x=260,y=170)
    ventana_login.mainloop()

# Ventana FACEID
def ventana_FACEID():
    global ventana_faceID
    ventana_faceID = Toplevel()
    ventana_faceID.title("FaceID")
    ventana_faceID.geometry ("330x250")
    ventana_faceID.iconbitmap('data/zorro.ico')

    Label (ventana_faceID, text="Acerque su rostro a la cámara", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (ventana_faceID, text="") .pack()

    #Abrir la cámara
    capture = cv2.VideoCapture(0)
    while (capture.isOpened()):
        ret, frame = capture.read()
        cv2.imshow('webCam',frame)
        if (cv2.waitKey(1) == ord('s')):
            break
    capture.release()
    cv2.destroyAllWindows()

    Label(ventana_faceID, text="").pack()
    '''
    Button(ventana_faceID, text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), command = verifica_login,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228').pack()
    '''
    Label(ventana_faceID, text="").pack()

# Ventana Gerente
def ventana_gerente(carnet):
    ventana_login.destroy()
    global ventana_gerente
    ventana_gerente = Toplevel()
    ventana_gerente.title("Ventana Gerente")
    ventana_gerente.geometry ("500x350")
    ventana_gerente.iconbitmap('data/zorro.ico')

    Label (ventana_gerente, text="Bienvenido Gerente", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (ventana_gerente, text="").pack()
    Button(ventana_gerente, text="Acceder al chat", width = "15", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    command=lambda:exito_login(carnet), foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()
    Label (ventana_gerente, text="").pack()
    Button(ventana_gerente, text="Registrar", width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color, command=nuevo_registro,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()
    Label (ventana_gerente, text="").pack()
    #Imagen
    rocket1 = PhotoImage(file='data/zorro.png').subsample(3,3)
    Label(ventana_gerente, image=rocket1).place(x=70,y=140)

# Función verificar identidad Login
def verifica_login(event):
    Dataset = leer_datos()
    global carnet
    carnet = verifica_usuario.get()
    entrada_login_usuario.delete(0, END)
    #El auxiliar es para que no de el mensaje de error si entra a gerente
    aux=1
    #guardando el dia en una variable
    dia = datetime.today().weekday()
    for idx, depar, genero in zip(Dataset["RFid"],Dataset["Departamento"], Dataset["Genero"]):
        if int(str(idx)) == int(carnet):
            if str(depar) == "Gerente":
                ventana_gerente(carnet)
                aux=0
            else:
                if str(genero) == "Masculino" and dia == 2 or str(genero) == "Femenino" and dia == 3:
                    usuario_descansa()
                    aux=0
                else:
                    exito_login(carnet)
                    aux=0
    if aux == 1:
        no_usuario()

# Función por si el usuario se equivocó en el usuario o no existe
def no_usuario ():
    ventana_login.destroy()
    
    global ventana_no_usuario
    ventana_no_usuario = Toplevel()
    ventana_no_usuario. title ("ERROR")
    ventana_no_usuario.geometry ("360x100")
    ventana_no_usuario.iconbitmap('data/zorro.ico')

    Label (ventana_no_usuario, text="Usuario no encontrado", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (text="").pack()
    Button (ventana_no_usuario, text="Ok", command=borrar_no_usuario, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()

#Funcion para mostrar que el usuario no puede ingresar por ser dia de descanso
def usuario_descansa ():
    ventana_login.destroy()
    
    global ventana_usuario_descansa
    ventana_usuario_descansa = Toplevel()
    ventana_usuario_descansa. title ("ERROR")
    ventana_usuario_descansa.geometry ("360x100")
    ventana_usuario_descansa.iconbitmap('data/zorro.ico')

    Label (ventana_usuario_descansa, text="Usuario no debe trabajar hoy", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (text="").pack()
    Button (ventana_usuario_descansa, text="Ok", command=borrar_usuario_descansa, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()

# Función por si el usuario accedio correctamente
def exito_login(carnet):
    ventana_principal.destroy()
    #Abrir Rocket
    fecha = time.strftime("%d/%m/%y")
    hora_llegada = time.strftime("%H:%M")
    guardar_fecha(fecha, hora_llegada, carnet)
    #os.system('python cliente.py')
    nombre = obtener_nombre(carnet)
    #desconexion(carnet)
    cliente(carnet, nombre)

def borrar_no_usuario():
    ventana_no_usuario.destroy()

def borrar_usuario_descansa():
    ventana_usuario_descansa.destroy()

#Main
ventana_inicio()