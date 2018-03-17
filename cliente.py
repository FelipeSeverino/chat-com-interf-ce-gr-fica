from tkinter import *
from socket import *
from threading import Thread


class classeReceber:
    def __init__(self, server):
        self.server = server
        self.data = ""
        
        th = Thread(target=self.thread1,args=())
        th.start()

    def thread1(self):
        while True:
            receber = self.server.recv(1024)
            self.data = receber.decode()

class software:
    def __init__(self, ip, port):
        self.end_server = ip
        self.port_server = port
        
        self.master = Tk()
        self.master.title("Cliente")
        self.master.geometry("500x500+0+0")

        self.ct = 0   #Verifica se o  socket já existe
        self.componentes()

    def componentes(self):
        self.btn_conexao = Button(self.master, text="Conectar-se com o servidor")
        self.btn_conexao.bind("<Button-1>", self.funcConectar)
        self.btn_conexao.place(x=165, y=10)

        self.btn_enviarMsg = Button(self.master, text="Enviar")
        self.btn_enviarMsg.bind("<Button-1>", self.funcEnviarMsg)
        self.btn_enviarMsg.place(x=20, y=85)

        self.txt_enviarMsg = Entry(self.master, width=60)
        self.txt_enviarMsg.place(x=80, y=90)

        self.texto = Text(self.master, width=49, height=17)
        self.texto.place(x=50, y=200)


    def funcConectar(self, evento):
        self.sockObj = socket(AF_INET, SOCK_STREAM)
        self.sockObj.connect((self.end_server, self.port_server))
        self.texto.insert(INSERT, "Sucesso ao conectar-se com o servidor\n")
        self.ct = 1
        
        th1 = Thread(target = self.funcAbrirClasseReceber, args=())
        th1.start()
        
    def funcEnviarMsg(self, evento):
        if self.ct == 0:
            self.texto.insert(INSERT, "Você precisa conectar-se ao servidor primeiro")
        else:
            mensagem = self.txt_enviarMsg.get()
        try:
            self.sockObj.send(mensagem.encode("utf-8"))
            self.texto.insert(INSERT, "Você: {}\n".format(mensagem))
        except:
            self.texto.insert(INSERT, "Erro\n")

    def funcAbrirClasseReceber(self):
        self.carreg = classeReceber(self.sockObj)
        
        th2 = Thread(target = self.funcReceber, args=())
        th2.start()
        
    def funcReceber(self):
        while True:
            if self.carreg.data != "":
                self.data = "Ele: {}\n".format(self.carreg.data)
                self.texto.insert(INSERT, self.data)
                self.carreg.data = ""
        
rodando = software("127.0.0.1", 80) #(ip do servidor, porta)
print("oi")
rodando.master.mainloop()
