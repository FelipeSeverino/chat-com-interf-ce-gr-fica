from tkinter import *
from socket import *
from threading import Thread

        
class software:
    def __init__(self):
        self.master = Tk()
        self.master.title("Chat server")
        self.master.geometry("500x500+0+0")

        self.ip = "127.0.0.1"
        self.port = 80
        self.ct = 0 #0 = sem conexão, 1 = conectado
        self.data = ""

        self.componentes()

    def componentes(self):
        self.btnAbrirSv = Button(self.master, text = "Abrir servidor")
        self.btnAbrirSv.bind("<Button-1>", self.funcAbrirSv)
        self.btnAbrirSv.place(x=200, y=10)

        self.texto = Text(self.master, width=56, height=15)
        self.texto.place(x = 20, y=200)

        self.btn_enviarMsg = Button(self.master, text="Enviar")
        self.btn_enviarMsg.bind("<Button-1>", self.funcEnviarMsg)
        self.btn_enviarMsg.place(x=20, y=85)

        self.txt_enviarMsg = Entry(self.master, width=60)
        self.txt_enviarMsg.place(x=80, y=90)

    def funcAbrirSv(self, evento):
        self.sockObj = socket(AF_INET, SOCK_STREAM)
        self.sockObj.bind((self.ip, self.port))
        self.sockObj.listen(1)

        self.texto.insert(INSERT, "Servidor aberto\n")
        print("Servidor aberto")

        thrAcharConexao = Thread(target = self.funcAcharConexao, args=()) 
        thrAcharConexao.start()

    def funcAcharConexao(self):
        self.endereço = ""
        
        while True:
            self.conexao, self.endereço = self.sockObj.accept()
            if self.endereço != None:
                print("Conectado com {}".format(self.endereço[0]))
                self.ct = 1
                self.funcReceber()
                break

    def funcReceber(self):
        while True:
            self.data = self.conexao.recv(1024)
            if self.data != None:
                print("Ele: {}".format(self.data.decode()))
                self.texto.insert(INSERT, "Ele: {}\n".format(self.data.decode()))

    def funcEnviarMsg(self, evento):
        if self.ct == 1:
            mandar = self.txt_enviarMsg.get().encode()
            self.conexao.send(mandar)
            self.texto.insert(INSERT, "Você: {}\n".format(mandar.decode()))
            print("Você: {}".format(mandar.decode()))
        else:
            self.texto.insert(INSERT, "Abra o servidor e espera que alguem conecte-se a você")
            print("Abra o servidor e espera que alguem conecte-se a você\n")
if __name__ == "__main__":
    rodando = software()
    rodando.master.mainloop()
