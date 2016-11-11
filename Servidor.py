#!/usr/bin/env python
# encoding: utf-8
 
from threading import Thread
import socket, os

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket (TCP)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código
s.bind((HOST, PORT)) #liga o socket com IP e porta
s.listen(1) #espera chegar pacotes na porta especificada
conn, addr = s.accept()#Aceita uma conexão

print 'Connectado ao', addr
print "Servidor funcionado com o PID", os.getpid()
print "Esperando pelos clientes\n"



a = conn.recv(1024) #Cliente querendo cadastrar
print a

user=a.split(",")
print user
""""
print a

b = conn.recv(1024) #Recebe nome do servidor

print b

c = conn.sendall('ok') #Não é repetido


b = conn.recv(1024) #Recebe senha do servidor

print b

b = conn.recv(1024) #Recebe telefone do servidor

print b

b = conn.recv(1024) #Recebe endereço do servidor

print b
"""

"""
class usuario:

	def __init__(self, nome, telefone, endereco, email, senha):

"""










