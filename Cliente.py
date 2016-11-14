#!/usr/bin/env python
# encoding: utf-8


import socket, os, time

#Rotina para testar se o valor é válido ##
# Sintaxe: teste("variável de input","comprimento mínimo da variável digitada")
def testa_entrada(valor,l):
	while 1:
		try:
			if len(valor) <= l: #Se o valor digitado for menor que o tamanho mínimo ele executa uma exceção
				raise
			break	#Se o valor for válido, ele quebra o loop
		except Exception, err:
			valor=raw_input('Valor inválido, digite novamente\n')	#Exceção pelo valor abaixo do mínimo determinado
	return valor #retorna valor válido

if __name__ == '__main__':  ###Programa principal
	HOST = raw_input('Digite o IP do servidor de leilão\n') # O host remoto. Nesse caso a saída precisa ser uma string
	PORT = input('Digite a porta usada pelo servidor de leilão\n') # A mesma porta usada pelo servidor de leilão
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código

	while 1: #loop para o cliente não travar caso o servidor não tenha sido aberto
		try:
			soc.connect((HOST, PORT))  #Abre uma conexão com IP e porta especificados
			break
		except:
			time.sleep(1)

	print "Você está conectado ao servidor\n"

	while 1:
		# Mensagem para o cliente digitar o que ele deseja fazer
		# Loop fica rodando até o cliente digitar '0' ou '1'
		while 1:
			c = raw_input('Digite 0 para cadastrar um novo usuário ou 1 para logar em um usuário já existente\n')
			if (c != '1') and (c != '0'):
				print "Valor inválido\n"
			else:
				break

		if c== '0': # Cliente escolhe cadastrar novo usuário
			print "---------Cadastro---------"
			while 1:  #Laço do cadastro
				nome = raw_input('Digite o nome do novo usuário:\n')  # Armazena a resposta do usuário na variável 'nome'
				nome = testa_entrada(nome, 0)  # Rotina para testar se a entrada é um valor não nulo

				telefone = raw_input('Digite o telefone do novo usuário.\nEx: xxxx-xxxx:\n')
				# Armazena a resposta do usuário na variável 'telefone'
				telefone = testa_entrada(telefone, 7)  # Rotina para testar se o telefone possui mais que 7 dígitos

				ender = raw_input(
					'Digite o endereço do novo usuário:\n')  # Armazena a resposta do usuário na variável 'ender'
				ender = testa_entrada(ender, 0)  # Rotina para testar se a entrada é um valor não nulo

				email = raw_input(
					'Digite o email do novo usuário:\n')  # Armazena a resposta do usuário na variável 'email'
				email = testa_entrada(email, 0)  # Rotina para testar se a entrada é um valor não nulo

				senha = raw_input('Digite a nova senha de no mínimo 4 dígitos:\n')
				# Armazena a resposta do usuário na variável 'senha'
				senha = testa_entrada(senha, 3)  # Rotina para testar se a entrada é um valor não nulo
				soc.sendall('Adiciona_usuario' + "," + str(nome) + "," + str(telefone) + "," + str(ender) + "," + str(email) + "," + str(senha))
				# Envia parâmetros para o servidor
				print "cheguei"
				re = soc.recv(1024)  # Recebe resposta do servidor
				if re == 'ok':
					print('Usuário cadastrado com sucesso.\n')
					break
				else:
					print('Nome de usuário já utilizado\n')
		else:
			print "---------Login---------"
			while (1):
				nome = raw_input('Digite o nome do usuário:\n')
				senha = raw_input('Digite sua senha:\n')
				soc.sendall("Faz_login"+","+nome+","+senha)
				rec = soc.recv(1024)
				if rec == 'ok':
					print('Usuário logado com sucesso')
					break
				else:
					print('Usuário não cadatrado ou dados incorretos\n')
		break

print "Dentro do leilão"





