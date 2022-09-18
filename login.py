from tkinter import *
import os
import tkinter
import tkinter.font as tkFont
pestas_color='#dd5228'

def ventana_inicio():
    global ventana_principal
    ventana_principal=Tk()
    ventana_principal.geometry("300x250")#Dimension
    ventana_principal.title("Rocket")#Titulo
    ventana_principal.iconbitmap('data/zorro.ico')
    Label (text="Escoja su opción", bg="white", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (text="").pack()
    Button(text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color, command=login,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()
    Label (text="").pack()
    Button(text="Registrarse", width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color, command=registro,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()
    Label (text="").pack()
    ventana_principal.mainloop()

def registro():
    global ventana_registro
    ventana_registro = Toplevel(ventana_principal)
    ventana_registro.title ("Registro")
    ventana_registro.geometry ("300x250")
    ventana_registro.iconbitmap('data/zorro.ico')

    global nombre_usuario
    global clave
    global entrada_nombre
    global entrada_clave
    nombre_usuario = StringVar ()
    clave = StringVar ()

    Label (ventana_registro, text="Introduzca datos", bg="white", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (ventana_registro, text="").pack()
    etiqueta_nombre = Label (ventana_registro, text="Nombre de usuario * ")
    etiqueta_nombre .pack()
    entrada_nombre = Entry (ventana_registro, textvariable=nombre_usuario)
    entrada_nombre .pack()
    etiqueta_clave = Label (ventana_registro, text="Contraseña * ")
    etiqueta_clave.pack()
    entrada_clave = Entry(ventana_registro, textvariable=clave, show="*")
    entrada_clave.pack()
    Label (ventana_registro, text="").pack()
    Button(ventana_registro, text="Registrarse", width = "10", height = "1", font = ("Helvetica 12 bold"), command = registro_usuario,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228').pack()

def registro_usuario():
    usuario_info = nombre_usuario.get()
    clave_info = clave.get ()

    file = open(usuario_info, "w")
    file.write (usuario_info + "n")
    file.write(clave_info)
    file.close()

    entrada_nombre.delete (0, END)
    entrada_clave.delete(0, END)

    Label (ventana_registro, text="Registro completado con éxito", fg="green", font=("calibri", 11)).pack()

def login ():
    global ventana_login
    ventana_login = Toplevel (ventana_principal)
    ventana_login.title("Acceso a la cuenta")
    ventana_login.geometry ("400x250")
    ventana_login.iconbitmap('data/zorro.ico')

    Label (ventana_login, text="Introduzca nombre de usuario y contraseña", bg="white", fg="#dd5228",
    font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (ventana_login, text="") .pack()

    global verifica_usuario
    global verifica_clave

    verifica_usuario = StringVar()
    verifica_clave = StringVar ()

    global entrada_login_usuario
    global entrada_login_clave

    Label (ventana_login, text="Nombre usuario * ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable = verifica_usuario)
    entrada_login_usuario.pack()
    Label(ventana_login, text="Contraseña * ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verifica_clave, show= '*')
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(ventana_login, text="Acceder", width = "10", height = "1", font = ("Helvetica 12 bold"), command = verifica_login,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228').pack()

def verifica_login():
    usuariol = verifica_usuario.get ()
    clavel = verifica_clave.get()
    entrada_login_usuario.delete(0, END)
    entrada_login_clave.delete(0, END)

    lista_archivos = os.listdir()
    if usuariol in lista_archivos:
        archivol = open(usuariol, "r")
        verifica = archivol.read().splitlines ()
        if clavel in verifica:
            exito_login()
        else:
            no_clave()
    else:
        no_usuario()

def no_usuario ():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel (ventana_login)
    ventana_no_usuario. title ("ERROR")
    ventana_no_usuario.geometry ("360x100")
    ventana_no_usuario.iconbitmap('data/zorro.ico')
    Label (ventana_no_usuario, text="Usuario no encontrado", bg="white", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
    Label (text="").pack()
    Button (ventana_no_usuario, text="Ok", command=borrar_no_usuario, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()

def exito_login():
    global ventana_exito
    ventana_exito = Toplevel (ventana_login)
    ventana_exito.title ("Exito")
    ventana_exito.geometry ("350x100")
    ventana_exito.iconbitmap('data/zorro.ico')
    Label (ventana_exito, text="Login exitoso", bg="white", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (text="").pack()
    Button (ventana_exito, text="OK", command=borrar_exito_login, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228') .pack()
    #Abrir Rocket
    os.system('python cliente.py')

def no_clave():
    global ventana_no_clave
    ventana_no_clave = Toplevel (ventana_login)
    ventana_no_clave.title ("ERROR")
    ventana_no_clave.geometry ("350x100")
    ventana_no_clave.iconbitmap('data/zorro.ico')
    Label (ventana_no_clave, text="Contraseña incorrecta", bg="white", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)).pack()
    Label (text="").pack()
    Button (ventana_no_clave, text="Ok", command=borrar_no_clave, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
    foreground = "white", activebackground = 'white', activeforeground = '#dd5228') .pack()

def borrar_exito_login():
    ventana_exito.destroy()

def borrar_no_clave():
    ventana_no_clave.destroy()

def borrar_no_usuario():
    ventana_no_usuario.destroy()

ventana_inicio()
