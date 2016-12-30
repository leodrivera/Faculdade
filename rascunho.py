#!/usr/bin/env python
# encoding: utf-8
import datetime, time
"""
print time.time()
now = datetime.datetime.now()
print now.year
print now.month
print now.day
'%d' % (42,)
#print now.hour
print '%f' % (now.hour,)
print now.minute
print now.second

hora_leilao = "11/12/2016 03:20:43"
#hora_leilao = str(i.dia) + '/' + str(i.mes) + '/' + str(i.ano), str(i.hora) + ':' + str(i.minuto) + ':' + str(i.segundo)
hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
hora_leilao = time.mktime(hora_leilao.timetuple())
#if time.time() - float(hora_leilao)
print hora_leilao
print time.time()

if hora_leilao-time.time() <= 30*60:
    print 'é menor'
else:
    print 'não é menor'

arquivo = open('leiloes_futuros.txt')  # atualizando txt com valor dos leilões ainda não terminados
a=arquivo.readlines()
print a
print a[1]
print a[0][0], a[1][0]
"""

temp = datetime.datetime.now()  # aquisição da hora atual e transformação em segundos
agora = str(temp.day) + '/' + str(temp.month) + '/' + str(temp.year) + ' ' + str(temp.hour) + ':' + str(
    temp.minute) + ':' + str(temp.second)
agora = datetime.datetime.strptime(agora, "%d/%m/%Y %H:%M:%S")
agora = time.mktime(agora.timetuple())

agora_rapido=time.time()

print 'Jeito trabalhoso:', agora
print 'Jeito trabalhoso:', agora_rapido