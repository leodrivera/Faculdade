#!/usr/bin/env python
# encoding: utf-8

from time import time, sleep
import socket, os, threading

#Classe onde ficam armazenadas as informações do usuário
class user:
    nome = None
    telefone = 0
    endereco = None
    email = None
    senha = None
    socket = None

    def __init__(self, nome, telefone, endereco, email, senha):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.email = email
        self.senha = senha
        self.socket = None

    # Registrar usuário em clientes.txt
    def arquivar_usuario(self):
        f = open('clientes.txt','a') # Escreve as linhas a partir da útlima linha escrita
        f.write(self.nome + ',' + self.telefone + ',' + self.endereco + ',' + self.email + ',' + self.senha+'\n')

class controle_usuarios:
    lista_usuario = []

    def adc_usuario(self,usuario):
        self.lista_usuario.append(usuario)
        usuario.arquivar_usuario() # adição do usuário ao arquivo .txt
    def retorna_usuario(self,nome):
        for i in self.lista_usuario:
            if i.nome == nome:
                s=i
        return s

    def imprime(self):
        print 'Dentro do txt tem'
        for i in self.lista_usuario:
            print i.nome

    def __init__(self): #metodo para carregar usuários do txt
        print 'inicia controle de usuários'
        try:  # Caso o arquivo 'clientes.txt' não exista, ele abre uma exceção de IOError e passa
            f = open('clientes.txt')  # Abre o arquivo clientes
            for linha in f:
                linha = linha.split(',')
                usuario = user(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]),str(linha[4].strip()))
                self.lista_usuario.append(usuario)
            self.imprime()
        except IOError:
            pass
    def checar_nome_existente(self,usuario):
        resp=0
        for i in self.lista_usuario:
            if i.nome==usuario:
                resp=1
                break
        return resp
    def checa_senha(self,nome,senha):
        s=0
        for i in self.lista_usuario:
            if i.nome == nome:
                if senha == i.senha:
                    s=1
                    break
        return s
    def add_socket(self,nome, socket):
        for i in self.lista_usuario:
            if i.nome == nome:
                i.socket=conn





#Servidor Thread
def servidor(conn):
    print 'Conectado por', addr, "\n"
    global controle, logado
    while 1:
        resp = conn.recv(1024)  # Cliente dizendo se quer cadastrar ou fazer login, com seus respectivos parâmetros
        if not resp: break #Sai do loop caso valor seja nulo ou 0
        a = resp.split(",") #Informações do usuário separados na lista 'a'
        #print "Recebi"
        if a[0] == 'Adiciona_usuario':
            #print "entrei no if"
            while 1: #Fica no loop para caso o nome seja repetido, ele tentar registrar novamente
                flag = controle.checar_nome_existente(a[1]) #Checar se o nome já foi cadastrado
                #print "Chequei nome"
                if flag == 1: #Se o nome for repetido, ele manda uma resposta ao cliente
                    conn.sendall('not_ok')
                    sleep(1)
                    conn.sendall('cl_usado')

                else:
                    nome = user(a[1],a[2],a[3],a[4],a[5]) # crio objeto 'nome' da classe usuário
                    nome.socket=conn
                    print "criei objeto"
                    controle.adc_usuario(nome) #adc usuário ao controle
                    controle.add_socket(a[1], conn)

                    logado = controle.retorna_usuario(a[1])
                    print "arquivei usuario"
                    conn.sendall('ok')
                break

        elif a[0] == 'Faz_login':
            print 'Faz_loguin acionado'
            while 1: #Fica no loop para caso a ele erre alguma coisa, tentar novamente
            #Se o nome que ele digitou for igual ao nome e a senha
            # forem iguais as que tenho no regsitro, ele faz o login
            ## print "Entrei login"
            #nome1 = globals()[a[1]].nome #Como fazer a comparação direto?
                k=controle.checar_nome_existente(a[1])
                print k
                if k==0:
                    print 'usuário inexistente'
                    conn.sendall('not_ok')
                    #sleep(1)
                    conn.sendall('inexis')
                    resp = conn.recv(1024)
                    a = resp.split(",")  # Informações do usuário separados na lista 'a'

                elif controle.checa_senha(a[1],a[2])==0:
                    print 'senha incorreta'
                    conn.sendall('not_ok')
                    #sleep(1)
                    conn.sendall('err_senha')
                    resp = conn.recv(1024)
                    a = resp.split(",")  # Informações do usuário separados na lista 'a'
                else:
                    print 'loguin correto'


                    controle.add_socket(a[1],conn)

                    logado=controle.retorna_usuario(a[1])

                    print "O socket do cliente foi armazenado:", #globals()[a[1]].socket

                    conn.sendall('ok')
                    # Perguntar se mando essa mensagem para o cliente ou se é só para mandar
                    # o not_ok
                    break  # sai do 1º while

#Tenho que criar um segundo Thread para o leilao


if __name__ == '__main__':  ###Programa principal

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50000              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket (TCP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código
    s.bind((HOST, PORT)) #liga o socket com IP e porta

    print "Servidor funcionado"
    print "Esperando pelos clientes\n"
    controle = controle_usuarios()  # carrega os usuarios que estavam no clientes.txt
    clientes=0
    logado=None
    while 1:
        s.listen(1)
        conn, addr = s.accept()  # Aceita uma conexão
        clientes += 1
        print "Número de clientes conectados", clientes
        t = threading.Thread(target=servidor, args=(conn,))
        t.start()
