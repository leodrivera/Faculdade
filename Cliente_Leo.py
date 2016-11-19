#!/usr/bin/env python
# encoding: utf-8


import socket, os, time

#Rotina para testar se o valor é válido ##
# Sintaxe: teste("variável de input","comprimento mínimo da variável digitada","Variável para teste de número","comprimento máximo")
def testa_entrada(valor,l,num=0,max=100):
    while 1:
        try:
            if (num == 'numero'): #Para checar se o valor inserido é um número, caso seja necessário
                valor = float(valor) #Transforma string em float. Se o valor for inteiro ou float, ele continua. Se for
                if max == 100:       #string, ele abre exceção. Caso o argumento max não tenha sido definido, ele sai do loop.
                    break
                elif len(str(int(valor))) > max:#Se o valor digitado for maior que o tamanho máximo, ele executa uma exceção.
                    raise                      #Caso contrário, ele transforma valor em um inteiro e sai do loop depois.
                else:
                    valor=int(valor)         #Eu transformo ele em um inteiro por causa das datas
            if len(str(valor)) <= l:   # Para a comparação ser correta, preciso conveter o valor(que está em float)
                raise                       # em str por causa do len
            else:                           #Se o valor digitado for menor que o tamanho mínimo ele executa uma exceção
                break	            #Quebra o loop
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
			c = raw_input('Digite:\n 0 para cadastrar um novo usuário\n 1 para logar em um usuário já existente\n')
			if (c != '1') and (c != '0'):
				print "Valor inválido\n"
			else:
				break

		if c== '0': # Cliente escolhe cadastrar novo usuário
			logged = 0 #Variável indicando que usuário não está logado
			print "---------Cadastro---------"
			while 1:  #Laço do cadastro
				nome = raw_input('Digite o nome do novo usuário:\n')  # Armazena a resposta do usuário na variável 'nome'
				nome = testa_entrada(nome, 0)  # Rotina para testar se a entrada é um valor não nulo

				telefone = raw_input('Digite o telefone do novo usuário.\nEx: xxxxxxxx:\n')
				# Armazena a resposta do usuário na variável 'telefone'
				telefone = testa_entrada(telefone, 7, 'numero')  # Rotina para testar se o telefone possui mais que 7 dígitos

				ender = raw_input('Digite o endereço do novo usuário:\n')  # Armazena a resposta do usuário na variável 'ender'
				ender = testa_entrada(ender, 0)  # Rotina para testar se a entrada é um valor não nulo

				email = raw_input('Digite o email do novo usuário:\n')  # Armazena a resposta do usuário na variável 'email'
				email = testa_entrada(email, 0)  # Rotina para testar se a entrada é um valor não nulo

				senha = raw_input('Digite a nova senha de no mínimo 4 dígitos:\n')
				# Armazena a resposta do usuário na variável 'senha'
				senha = testa_entrada(senha, 3)  # Rotina para testar se a entrada é um valor não nulo
				soc.sendall('Adiciona_usuario' + "," + str(nome) + "," + str(telefone) + "," + str(ender) + "," + str(email) + "," + str(senha))
				# Envia parâmetros para o servidor
				#print "cheguei"
				re = soc.recv(1024)  # Recebe resposta do servidor
				if re == 'ok':
					print('Usuário cadastrado com sucesso.\n')
					break
				else:
					print('Nome de usuário já utilizado\n')
		else:
			print "---------Login---------"
			while (1):
				nome = raw_input('Digite o nome do usuário:\n') #Armazena o nome do usuário na variável nome
				senha = raw_input('Digite sua senha:\n') #Armazena a senha do usuário na variável senha
				soc.sendall("Faz_login"+","+nome+","+senha) #Envia as informações para o servidor
				rec = soc.recv(1024) #Recebe as respostas do servidor
				if rec == 'ok': #Se a resposta for ok
					print('Usuário logado com sucesso')
					logged = 1 #Indica que está logado
					break #Sai do 'Login' loop
				else:
					print('Usuário não cadatrado ou dados incorretos\n')
		if logged == 1: #Se o usuário estiver logado, ele sai do loop principal
			break #Sai do loop principal


	print "---------Bem vindo ao sistema de leilão---------\nDiga o que deseja fazer:\n"
	c=raw_input('1 para Lançar um novo produto\n')
	if c == '1': # Cliente escolhe lançar novo produto
		print "---------Lançar Produto---------"
		while 1:  #Laço do Lança_Produto
			nome = raw_input('Digite o nome do novo produto:\n')  # Armazena a resposta do usuário na variável 'nome'
			nome = testa_entrada(nome, 0)  # Rotina para testar se a entrada é um valor não nulo

			descricao = raw_input('Digite a descricao do novo produto.\n')
			# Armazena a resposta do usuário na variável 'descricao'
			descricao = testa_entrada(descricao, 0)  # Rotina para testar se a entrada é um valor não nulo

			lance_min = raw_input('Digite o lance mínimo para o produto:\n')
			# Armazena a resposta do usuário na variável 'lance_min'
			lance_min = testa_entrada(lance_min, 0, 'numero')
			# Rotina para testar se a entrada é um valor não nulo e se é um número

			dia = raw_input('Digite o dia do leilão:\nEx: xx:\n')  # Armazena a resposta do usuário na variável 'dia'
			dia = testa_entrada(dia, 0, 'numero',2)  # Rotina para testar se a entrada é um valor compatível

			mes = raw_input('Digite o mês do leilão:\nEx: xx:\n')  # Armazena a resposta do usuário na variável 'mes'
			mes = testa_entrada(mes, 0, 'numero',2)  # Rotina para testar se a entrada é um valor compatível

			ano = raw_input('Digite o ano do leilão:\nEx: xxxx:\n')  # Armazena a resposta do usuário na variável 'ano'
			ano = testa_entrada(ano, 3, 'numero',4)  # Rotina para testar se a entrada é um valor compatível

			hora = raw_input('Digite a hora do leilão:\nEx: xx:\n')  # Armazena a resposta do usuário na variável 'hora'
			hora = testa_entrada(hora, 0, 'numero',2)  # Rotina para testar se a entrada é um valor compatível

			minuto = raw_input('Digite os minuto do leilão:\nEx: xx:\n')  # Armazena a resposta do usuário na variável 'minuto'
			minuto = testa_entrada(minuto, 0, 'numero',2)  # Rotina para testar se a entrada é um valor compatível

			segundo = raw_input('Digite os segundo do leilão:\nEx: xx:\n')  # Armazena a resposta do usuário na variável 'segundo'
			segundo = testa_entrada(segundo, 0, 'numero',2)  # Rotina para testar se a entrada é um valor compatível

			tempo_max = raw_input('Digite tempo máximo sem lances, em segundos, do leilão:\n')
			# Armazena a resposta do usuário na variável 'tempo_max'
			tempo_max = testa_entrada(tempo_max, 0, 'numero')  # Rotina para testar se a entrada é um valor compatível

			soc.sendall('Lanca_produto' + "," + str(nome) + "," + str(descricao) + "," + str(lance_min) + "," + str(dia) + "," +\
				str(mes) + "," + str(ano) + "," + str(hora) + "," + str(minuto) + "," + str(segundo) + "," + str(tempo_max))
			#Envia a mensagem para o cliente

			resp = soc.recv(1024)
			if resp == 'ok':
				print "Produto lançado com sucesso\n"
				break
			else:
				print "Ocorreu algum erro. Tente novamente\n"








