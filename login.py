from tkinter import *
import os
import tkinter
import tkinter.font as tkFont
from data import *
import time
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

# Ventana de registro
def registro():
    global ventana_registro
    ventana_registro = Toplevel(ventana_principal)
    ventana_registro.title ("Registro")
    ventana_registro.geometry ("300x250")
    ventana_registro.iconbitmap('data/zorro.ico')

    #Acceso al Google Sheet

# Ventana acceder/Login
def login ():
    global ventana_login
    ventana_login = Toplevel()
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry ("400x250")
    ventana_login.iconbitmap('data/zorro.ico')

    Label (ventana_login, text="Acerque su carnet por el lector", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (ventana_login, text="") .pack()

    global verifica_usuario
    verifica_usuario = StringVar()
    global entrada_login_usuario

    Label (ventana_login, text="Carnet* ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable = verifica_usuario)
    entrada_login_usuario.pack()

    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), command = verifica_login,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228').pack()
    Label(ventana_login, text="").pack()
    #Gif
    rfid = PhotoImage(file='data/RFid.gif', master=ventana_login).subsample(4,4)
    Label(ventana_login, image=rfid).pack()

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
    rfid = PhotoImage(file='data/origami.png', master=ventana_gerente).subsample(4,4)
    Label(ventana_gerente, image=rfid).pack()

# Función verificar identidad Login
def verifica_login():
    Dataset = leer_datos()
    global carnet
    carnet = verifica_usuario.get()
    entrada_login_usuario.delete(0, END)
    #El auxiliar es para que no de el mensaje de error si entra a gerente
    aux=1
    for idx, depar in zip(Dataset["RFid"],Dataset["Departamento"]):
        if int(str(idx)) == int(carnet):
            if str(depar) == "Gerente":
                ventana_gerente(carnet)
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

# Función por si el usuario accedio correctamente
def exito_login(carnet):
    ventana_principal.destroy()
    #Abrir Rocket
    fecha = time.strftime("%d/%m/%y")
    print(fecha)
    hora_llegada = time.strftime("%H:%M:%S")
    print(hora_llegada)
    guardar_fecha(fecha, hora_llegada, carnet)
    os.system('python cliente.py')

def borrar_no_usuario():
    ventana_no_usuario.destroy()

#Main
ventana_inicio()