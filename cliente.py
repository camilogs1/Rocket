from data import *

def cliente(carnet, nombre):
    print("Cliente",carnet)
    from socket import AF_INET, socket, SOCK_STREAM
    from threading import Thread
    import tkinter
    from tkinter import VERTICAL
    import tkinter.font as tkFont
    from tkinter import messagebox
    import json

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
                    send(nombre)
                else:
                    msg_list.insert(tkinter.END, msg)
                    msg_list.see(tkinter.END)
                    #items = conectlist.get(0,last=len(lista))
                    #print(items, type(items))
            except OSError:  # Posiblemente el cliente ha abandonado el chat.
                break

    def send(nombre=" "):  # el evento se pasa por binders.
        #Maneja el envío de mensajes.

        msg = my_msg.get()
        msg= nombre+msg
        my_msg.set("")  # Borra el campo de entrada.
        client_socket.send(bytes(msg, "utf8"))
        if msg == "quit":
            client_socket.close()
            top.quit()

    def on_closing(event=None):
        #Esta función debe ser llamada cuando se cierra la ventana
        desconexion(carnet)
        my_msg.set("quit")
        send()

    #Creación pestaña
    top = tkinter.Tk()
    top.iconbitmap('data/zorro.ico')
    top.config(bg="white",bd=0)
    top.title("Rocket")
    label= tkinter.Label(top, text="Chat empresarial", bg="white", fg="#dd5228")
    label.configure(font=("Bahnschrift Light bold", 19,tkFont.BOLD))
    label.pack()

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
    send_button = tkinter.Button(top, text="Enviar", width = "10", height = "1", font = ("Helvetica 12 bold"), command=send,
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