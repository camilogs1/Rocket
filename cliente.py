from data import *
from tkinter import *
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import VERTICAL
import tkinter.font as tkFont
from tkinter import messagebox
import json

def cliente(carnet, nombre):
    print("Cliente",carnet)

    top = tkinter.Tk()
    top.iconbitmap('data/zorro.ico')
    top.config(bg="white",bd=0)
    top.title("Rocket")
    label= tkinter.Label(top, text="Chat empresarial", bg="white", fg="#dd5228")
    label.configure(font=("Bahnschrift Light bold", 19,tkFont.BOLD))
    label.pack()

    def receive():
        #Maneja la recepción de mensajes.
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                #print(msg)
                #fin
                try:
                    new = json.loads(msg)
                    conectlist.insert(tkinter.END,new)
                except:
                    pass
                if "está en linea." in msg:
                    #lista.append(msg)
                    conectlist.insert(tkinter.END, msg)
                    conectlist.itemconfigure(tkinter.END, bg="#00aa00", fg="#fff")
                    # items = conectlist.get()
                    # print(items, type(items))
                elif "ha dejado el chat" in msg:
                    #lista.append(msg)
                    conectlist.insert(tkinter.END, msg)
                    conectlist.itemconfigure(tkinter.END, bg="#ff0000", fg="#fff")
                    #items = conectlist.get(0,last=len(lista))
                    #print(items, type(items))
                    # items = conectlist.get()
                    # print(items, type(items))
                elif "Conectando..." in msg:
                    send()
                else:
                    msg_list.insert(tkinter.END, msg)
                    msg_list.see(tkinter.END)
                    #items = conectlist.get(0,last=len(lista))
                    #print(items, type(items))
            except OSError:  # Posiblemente el cliente ha abandonado el chat.
                break

    def login ():
        from tkinter import VERTICAL
        import tkinter.font as tkFont
        from tkinter import messagebox
    
        global ventana_login
        ventana_login = Toplevel()
        ventana_login.title("Acceso a la cuenta")
        ventana_login.geometry ("330x250")
        ventana_login.iconbitmap('data/zorro.ico')

        Label(ventana_login, text="Acerque su carnet por el lector", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
        Label(ventana_login, text="").pack()

        global verifica_usuario
        verifica_usuario = StringVar()
        global entrada_login_usuario

        #Label (ventana_login, text="Carnet* ").pack()
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
        ventana_login.mainloop()

    def borrar_no_usuario():
        ventana_no_usuario.destroy()
        login()
    
    def no_usuario ():
        ventana_login.destroy()
        pestas_color='#dd5228'
        
        global ventana_no_usuario
        ventana_no_usuario = Toplevel()
        ventana_no_usuario. title ("ERROR")
        ventana_no_usuario.geometry ("360x100")
        ventana_no_usuario.iconbitmap('data/zorro.ico')

        Label (ventana_no_usuario, text="Usuario no encontrado", fg="#dd5228", font=("Bahnschrift Light bold", 12,tkFont.BOLD)) .pack()
        Label (text="").pack()
        Button (ventana_no_usuario, text="Ok", command=borrar_no_usuario, width = "10", height = "1", font = ("Helvetica 12 bold"), bg=pestas_color,
        foreground = "white", activebackground = 'white', activeforeground = '#dd5228').pack()

    def verifica_login(event):
        Dataset = leer_datos()
        #si se daña es por esto
        #global carnet
        carnet = verifica_usuario.get()
        entrada_login_usuario.delete(0, END)
        #El auxiliar es para que no de el mensaje de error si entra a gerente
        aux=0
        for idx in Dataset["RFid"]:
            if int(str(idx)) == int(carnet):
                aux+=1
                client_socket.send(bytes(msg, "utf8"))
                client_socket.close()
                top.destroy()
        
        if aux ==0:
            no_usuario()


    def send(event=None):  # el evento se pasa por binders.
        #Maneja el envío de mensajes.
        #print("Este es nombre: ",nombre)
        nonlocal top
        global msg
        msg = my_msg.get()
        if msg == "":
            msg = nombre
        else: msg= msg
        my_msg.set("")  # Borra el campo de entrada.
        aux = 0
        if msg == "quit":
            login()
            desconexion(carnet)
            aux +=1
            #top.destroy()
        if aux == 0:
            client_socket.send(bytes(msg, "utf8"))

    def on_closing(event=None):
        #Esta función debe ser llamada cuando se cierra la ventana
        my_msg.set("quit")
        send()

    #Creación pestaña
    

    messages_frame = tkinter.Frame(top)
    conectadosframe = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # Para los mensajes que se envían.
    my_msg.set("")

    scrollbar = tkinter.Scrollbar(messages_frame, orient=VERTICAL)  # Para navegar por los mensajes anteriores.
    label2= tkinter.Label(top, text="Usuarios", bg="white", fg="#dd5228")
    label2.configure(font=("Bahnschrift Light bold", 10, tkFont.BOLD))
    label2.pack(side=tkinter.LEFT)
    label2.place(x=5,y=50)

    conectlist = tkinter.Listbox(conectadosframe, height=18, width=24)
    conectlist.pack(side=tkinter.RIGHT)
    #lista = ["."]
    #conectlist.insert(0, *lista)
    conectlist.pack(fill= "y")
    #items = conectlist.get(0,last=len(lista))
    #print(items, type(items))
    #conectlist.insert()

    conectadosframe.pack(side=tkinter.LEFT)

    scrollbar = tkinter.Scrollbar(messages_frame)  # Para navegar por los mensajes anteriores.

    # A continuación, los mensajes.
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    msg_list = tkinter.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set)
    scrollbar.config(command=msg_list.yview)
    msg_list.pack(expand=1)
    msg_list.pack(fill=tkinter.BOTH)
    messages_frame.pack(expand=1)
    messages_frame.pack(fill='both')

    entry_field = tkinter.Entry(top, textvariable=my_msg, width= 45, highlightbackground='black', highlightthickness=3)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Enviar", width = "10", height = "1", font = ("Helvetica 12 bold"), command= send,
    foreground = "white", bg = '#dd5228', activebackground = 'white', activeforeground = '#dd5228')
    send_button.pack()

    #conectados.pack()
    #conectados.place(x=0, y=0)

    top.protocol("WM_DELETE_WINDOW", on_closing)

    #----Ahora viene la parte del socket----
    #HOST = '172.20.10.10'
    HOST = 'localhost'

    # IP del servidor
    PORT = 55555

    if not PORT:
        PORT = 55555
    else:
        PORT = int(PORT)

    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Inicia la ejecución de la GUI.