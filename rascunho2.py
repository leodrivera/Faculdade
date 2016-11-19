#!/usr/bin/env python
# encoding: utf-8
"""
import datetime
now = datetime.datetime.now()
print now.year
print now.month
print now.day
'%d' % (42,)
#print now.hour
print '%f' % (now.hour,)
print now.minute
print now.second

"""
#Rotina para testar se o valor é válido ##
# Sintaxe: teste("variável de input","comprimento mínimo +1 da variável digitada","Variável para teste de número","comprimento máximo")
def testa_entrada(valor,l,num=0,max=100):
    while 1:
        try:
            if (num == 'numero'): #Para checar se o valor inserido é um número, caso seja necessário
                valor = float(valor) #Transforma string em float. Se o valor for inteiro ou float, ele continua. Se for
                                            #string, ele abre exceção.
                if len(str(int(valor))) > max:#Se o valor digitado for maior que o tamanho máximo, ele executa uma exceção.
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


#telefone = raw_input('Digite o telefone do novo usuário.\nEx: xxxxxxxx:\n')
# Armazena a resposta do usuário na variável 'telefone'
#telefone = testa_entrada(telefone, 7, 'numero')  # Rotina para testar se o telefone possui mais que 7 dígitos
#print "Telefone:", telefone

nome = raw_input('Digite o nome do novo produto:\n')  # Armazena a resposta do usuário na variável 'nome'
nome = testa_entrada(nome, 0)  # Rotina para testar se a entrada é um valor não nulo
print nome
"""
print lance_min

def testa_numero(message):
    def testa_int(message):
        try:
            userinput = int(input(message))a
            return count=1
        except NameError:
            return count=0
    def testa_float(message):
        try:
            userinput = float(input(message))
            return count=1
        except NameError:
            return count=0
    a=testa_int(message)
    b=testa_float(message)
    if (a+b) ==  1:
        return userinput
    type(a)

age = testa_numero('Digite o lance mínimo para o produto:\n')
print age
"""