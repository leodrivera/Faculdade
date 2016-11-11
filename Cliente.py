#!/usr/bin/env python
# encoding: utf-8


import socket, os, time

HOST = '127.0.0.1'    # The remote host
PORT = 50008              # The same port as used by the server
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código

while 1:
	try:
		soc.connect((HOST, PORT))  #Abre uma conexão com IP e porta especificados
		break
	except:
		time.sleep(1)

def teste(valor,l): # função para tratamento de erro de entrada de valores
	while 1:		
		try:	
			if len(valor) <= l: #Se o valor digitado for menor que o tamanho mínimo ele executa uma exceção
				raise
			break	#Se o valor for válido, ele quebra o loop
		except Exception, err:
			valor=raw_input('Valor inválido, digite novamente\n')	#Exceção pelo valor vazio
	return valor #retorna valor válido


c=raw_input('Digite 0 para cadatrar novo usuário ou 1 para logar em usuário já existente\n')

while (c != '1') and (c != '0'):
	c=raw_input('Digite 0 para cadatrar novo usuário ou 1 para logar em usuário já existente\n')

if c== '0': # Cadastro de novo usuário
	# soc.sendall('Adiciona_usuario')

	while 1:  #Laço do cadastro
		nome=raw_input('Digite o nome do novo usuário\n')
		nome=teste(nome,0) # Teste de entrada vazio
		soc.sendall(nome) # Envia nome para o servidor
		check = soc.recv(1024) #Recebe resposta se o nome é repetido ou não
		#if check == 'ok':
		#	print "Tá tranquilo, tá favorável"
		#	break # Se passar no teste, ele sai
		#print ('Nome existente.\n')
		senha=raw_input('Digite a nova senha de no mínimo 4 dígitos\n')
		senha=teste(senha,3) # Teste de entrada vazio
		#soc.sendall(senha) # Envia senha para o servidor
		telefone=raw_input('Digite o telefone do novo usuário.\nEx: xxxx-xxxx\n')
		telefone=teste(telefone,7) # Teste de entrada vazio
		#soc.sendall(telefone) # Envia telefone para o servidor
		ender=raw_input('Digite o endereço do novo usuário\n')
		ender=teste(ender,0) # Teste de entrada vazio
		#soc.sendall(end) # Envia endereço para o servidor
		soc.sendall('Adiciona_usuario'+","+nome+","+senha+","+ender)

		break



	








