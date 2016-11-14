#!/usr/bin/env python
# encoding: utf-8

"""
f1 = open("clientes.txt")
texto=f1.readlines()
print texto

usuario="Leo"

for i in range(len(texto)):
    if usuario+"\n" == texto[i]:
        print "linha",i
"""

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

    # Registrar usuário em clientes.txt
    def arquivar_usuario(self):
        f = open('clientes.txt', 'a') # Escreve as linhas a partir da útlima linha escrita
        f.write(self.nome + ',' + self.telefone + ',' + self.endereco + ',' + self.email + ',' + self.senha)
"""
try:  # Caso o arquivo 'clientes.txt' não exista, ele passa
  f = open('clientes.txt')
  for linha in f:
    print linha
    linha0, linha1, linha2, linha3, linha4 = linha.split(',')
    print linha0
    linha0 = user(str(linha[0]), str(linha[1]),str(linha[2]), str(linha[3]),str(linha[4]))
except IOError:
  pass

#print Leo.senha
#print arroz.nome
"""
Leo = user('1','2','3','4','5\n')
#Leo.arquivar_usuario()

g=open('clientes.txt')
for linha in g:
  linha=linha.split(',')
  print linha[4].strip()
