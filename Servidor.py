#!/usr/bin/env python
# encoding: utf-8
 
from threading import Thread, Lock
import socket, os

class usuario:
    nome = None
    telefone = 0
    endereco = None
    email = None
    senha = None

    def __init__(self, nome, telefone, endereco, email, senha):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha





class ctr_usuarios:
    lista_usuarios=[]
    def __init__(self):
        print'inicia lista de usuários'
    def recebe_usuario(self,usuarios):
        self.lista_usuarios.append(usuario)

    def checa_nomes(self,nome):
        resp='tem'
        for i in self.lista_usuarios:
            if nome==i:
                resp='n_tem'
        return resp


def servidor(conn):
    print 'Conectado por', addr, "\n"
    while 1:
        a = conn.recv(1024)  # Cliente querendo cadastrar com os dados contidos em a
        user = a.split(",")  # Informações do usuário separados na lista user
        print user

"""""

        if user[0] == 'Adiciona_usuario': # adiciona_usuario
            for i in range(nclientes):



                conn.sendall('not_ok'+'cl_usado')

            else:
"""""
            #texto.acquire()

            #texto.release()






            #login do usuario


if __name__ == '__main__':  ###Programa principal

    #Recupera variáveis
    try:
        f1 = open("clientes.txt")
        texto = f1.readlines()

    except IOError: pass

    HOST = '127.0.0.1'                 # Symbolic name meaning all available interfaces
    PORT = 50008              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket (TCP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código
    s.bind((HOST, PORT)) #liga o socket com IP e porta
    #s.listen(1) #espera chegar pacotes na porta especificada
    #conn, addr = s.accept()#Aceita uma conexão

    print "Servidor funcionado"
    print "Esperando pelos clientes\n"

    nclientes=0

    clientes={}

    while 1:
        print 'escutando'
        s.listen(1)
        conn, addr = s.accept()  # Aceita uma conexão
        nclientes += 1
        #PID.append(conn.recv(1024))  # Recebe o PID do cliente
        #print "Cliente conectado com o PID", PID[clientes - 1]
        print "Número de clientes conectados", nclientes
        t = Thread(target=servidor, args=(conn,))
        t.start()




    #print a

    #b = conn.recv(1024) #Recebe nome do servidor












