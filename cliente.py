from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
import tkinter
import tkinter.font as tkFont
from tkinter import messagebox
import json

def receive():
    #Maneja la recepción de mensajes.
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            #fin
            try:
                new = json.loads(msg)
                conectlist.insert(tkinter.END,new)
            except:
                pass
            if "Está en linea." in msg:
                conectlist.insert(tkinter.END, msg)
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:  # Posiblemente el cliente ha abandonado el chat.
            break

def send(event=None):  # el evento se pasa por binders.
    #Maneja el envío de mensajes.
    msg = my_msg.get()
    my_msg.set("")  # Borra el campo de entrada.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "quit":
        client_socket.close()
        top.quit()

def on_closing(event=None):
    #Esta función debe ser llamada cuando se cierra la ventana
    my_msg.set("quit")
    send()


#Usuarios Conectados
'''
def about():
    ventana_about = Toplevel()
    ventana_about.iconbitmap('data/origami.ico')
    ventana_about.config(bg = "white")
    ventana_about.title("Conectados")
    ventana_about.geometry("250x250+30+50")
    ventana_about.resizable(1,1)

    user_frame = tkinter.Frame(ventana_about)
    scrollbar = tkinter.Scrollbar(user_frame) 
    user_list = tkinter.Listbox(user_frame, height=20, width=80, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    user_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)

    user = client_socket.recv(BUFSIZ).decode("utf8")
    user_list.insert(tkinter.END, user)

    c = """Usuarios conectados:"""
    e1_descripcion = Label(ventana_about, text = c, width = 30, font = ("Helvetica 12"), bg = "white", justify = tkinter.LEFT, fg = "black")
'''


#fin

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
label2= tkinter.Label(top, text="Usuarios Conectados", bg="white", fg="#dd5228")
label2.configure(font=("Bahnschrift Light bold", 10, tkFont.BOLD))
label2.pack(side=tkinter.LEFT)
label2.place(x=5,y=50)

conectlist = tkinter.Listbox(conectadosframe, height=18, width=24)
conectlist.pack(side=tkinter.RIGHT)
conectlist.pack()
#conectlist.insert()
conectadosframe.pack(side=tkinter.LEFT)

scrollbar = tkinter.Scrollbar(messages_frame)  # Para navegar por los mensajes anteriores.

# A continuación, los mensajes.
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

msg_list = tkinter.Listbox(messages_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.config(command=msg_list.yview)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

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
HOST = '172.20.10.10' # IP del servidor
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