#!/usr/bin/env python
# encoding: utf-8

import socket, os, threading, datetime, time

class leilao: # Classe dos leilões
    identificador=0
    nome=' '
    descricao=' '
    lance_minimo=0
    lance_corrente=0
    vencedor_corrente=None
    conta_lances=0
    lance_vencedor=0
    hora_leilao=0
    hora_ultimo_lance=0
    dia=0
    mes=0
    ano=0
    hora=0
    minuto=0
    segundo=0
    tempo=0
    t_max=0
    dono=None
    data_venda=' '
    participantes=[]
    flag_de_situacao=0

    # Contrutor de novos leilões
    def __init__(self,nome, descricao,lance_minimo, dia, mes, ano, hora, minuto, segundo, t_max, dono):
        self.nome=nome
        self.descricao=descricao
        self.lance_minimo=float(lance_minimo)
        self.lance_corrente=float(lance_minimo) # protegida
        print 'lance da inicialização',self.lance_corrente
        self.vencedor_corrente='Aguardando o envio' # protegida

        hora_leilao = str(dia) + '/' + str(mes) + '/' + str(ano) + ' ' + str(hora) + ':' + str(minuto) \
                      + ':' + str(segundo)  # para verificação se data é no futuro
        hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
        hora_leilao = time.mktime(hora_leilao.timetuple())
        self.hora_leilao=hora_leilao
        self.conta_lances=0
        self.hora_ultimo_lance=hora_leilao # protegida
        self.lance_vencedor=float(lance_minimo)
        self.dia=dia
        self.mes=mes
        self.ano=ano
        self.hora=hora
        self.minuto=minuto
        self.segundo=segundo
        self.t_max=t_max
        self.dono=dono
        self.data_venda=' '
        self.participantes=[]
        self.flag_de_situacao=0

        # Método para salvar leilões nos arquivos txt
    def arquivar_leilao_futuro(self):
        f = open('leiloes_futuros.txt','a') # Escreve as linhas a partir da útlima linha escrita
        f.write(str(self.identificador)+','+self.nome+','+self.descricao+','+str(self.lance_minimo)+','\
        +str(self.dia)+','+ str(self.mes)+','+str(self.ano)+','+str(self.hora)+','+str(self.minuto)+','\
        +str(self.segundo)+','+str(self.t_max)+','+self.dono+'\n')
        f.close()

#Classe onde ficam armazenadas as informações do usuário
class user:
    nome = None
    telefone = 0
    endereco = None
    email = None
    senha = None
    socket1 = None
    socket2 = None
    indice = None
    mensagens_pendentes = []

    def __init__(self, nome, telefone, endereco, email, senha, soc, indice): #construtor da classe dos usuários
        self.nome = nome              # atributos dos usuários
        self.telefone = telefone      # |
        self.endereco = endereco      # |
        self.email = email            # |
        self.senha = senha            # |
        self.socket1 = soc            # |
        self.socket2 = None           # |
        self.indice = indice          # |
        self.mensagens_pendentes = [] # |


    # Registrar usuário em clientes.txt
    def arquivar_usuario(self):
        f = open('clientes.txt','a') # Escreve as linhas a partir da útlima linha escrita
        f.write(self.nome + ',' + self.telefone + ',' + self.endereco + ',' + self.email +
                ',' + self.senha+','+self.socket1+','+str(self.indice)+'\n')
        f.close()

class controle_geral: # Classe que controla os usários do sistema de leilão
    lista_usuario = []  # Atributo que lista todos os usuários já cadastrados
    onlines = []  #atributo que guarda os índices na lista_usuario dos usuários que estão online
    lista_leiloes_futuros=[]
    lista_leiloes_correntes=[] # atributo onde estarão os leilões iniciados para monitoramento
    inicios_de_leilao=[]

    def adc_usuario(self,usuario):  # Método para adicionar novo usuário à lista
        self.lista_usuario.append(usuario)           # Inclusão do usuário no atributo lista
        usuario.arquivar_usuario() # adição do usuário ao arquivo .txt
        return usuario.indice         # retorno do índice do usuário para uso do programa

    def retorna_usuario(self,nome,sock): #Método de busca de usuário para login
        s=None
        for i in self.lista_usuario: # Percorre atributo lista
            if i.nome == nome: # Preenche resposta com usuário quando encontrado
                i.socket1=sock
                s=i

                break
        return s  #retorna usuŕio quando encontrado ou vazio quando não encontrado

    def imprime_aquisicoes(self): # Método para printar usuários carregados do txt na inicialização
        print 'Dentro do .txt dos usuários tem:'
        for i in self.lista_usuario:
            print i.nome+i.socket1

        print '\nDentro do .txt dos leilões não terminados tem:'
        for i in self.lista_leiloes_futuros:
            print str(i.nome)+', pertecente a '+i.dono+' para dia: '+str(int(i.dia))\
                  +'/'+str(int(i.mes))+'/'+str(int(i.ano))+' as '+str(int(i.hora))+\
                  ':'+str(int(i.minuto))+'h'


    def __init__(self): #metodo para carregar usuários do txt
        self.onlines = []
        self.lista_usuario=[]
        self.inicios_de_leilao=[]
        print 'Iniciando controle de usuários...\n'
        try:  # Caso o arquivo 'clientes.txt' não exista, ele abre uma exceção de IOError e passa
            f = open('clientes.txt')  # Abre o arquivo clientes
            for linha in f: # Percorre todas as linhas do txt
                linha=linha.split(',')
                linha[0] = user(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3])
                                ,str(linha[4]),str(linha[5]+','+linha[6]),str(linha[7])) # Transforma linhas do txt em objetos da classe user
                self.lista_usuario.append(linha[0])
            f.close()
        except IOError:
            pass
        try: # Caso o arquivo 'clientes.txt' não exista, ele abre uma exceção de IOError e passa
            f = open('leiloes_futuros.txt')  # Abre o arquivo leilões não terminados
            for linha in f:  # Percorre todas as linhas do txt (leilões arquivados)
                c = linha.split(',')

                for i in range(3,10):  # Transforma strings de saída do txt em floats
                    c[i]=int(float(c[i]))

                if teste_de_data(c[4], c[5], c[6], c[7], c[8], c[9],0) == 1: # Verifica se a data e hora de início de leilões arquivados não expiraram
                    leilaao = leilao(str(c[1]), str(c[2]), str(c[3]), str(c[4]), str(c[5]), str(c[6]), \
                     str(c[7]), str(c[8]), str(c[9]), str(c[10]), str(c[11].strip()))
                    # Transforma linhas do txt em objetos da classe user. O último elemento precisa do .strip() por causa do \n
                    leilaao.identificador=c[0] #Salvando identificador do leilão
                    self.lista_leiloes_futuros.append(leilaao)

                    hora_leilao = str(c[4]) + '/' + str(c[5]) + '/' + str(c[6]) + ' ' + str(c[7]) + ':' + str(c[8]) \
                                  + ':' + str(c[9])  # para verificação se data é no futuro
                    hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
                    hora_leilao = time.mktime(hora_leilao.timetuple())

                    self.inicios_de_leilao.append([c[0], hora_leilao])


                else :
                    #aviso de que algum leilão perdeu a data de inicio com servidor off line
                    print '\nLeilão número '+str(c[0])+' teve momento de início perdido com servidor off-line\n'
            print self.inicios_de_leilao
        except IOError:
            pass
        self.imprime_aquisicoes()
        # Inicializa atributo de usuários onlines com lista vazia

    def checar_nome_existente(self,usuario,flag,senha): # Método que verifica se usuário existe quando flag = 0 e tmb testa se a senha dele é correta quando flag != 0
        resp=0
        for i in self.lista_usuario: # percorre atributo lista
            if i.nome==usuario: # verifica se usuário é usuário em questão da lista
                if flag == 0: # encontrado o nome do usuário, verifica se é preciso teste de senha
                    resp=1
                elif i.senha == senha:  #verifica se senha é correta
                    resp=1
                    break
        return resp

    def add_socket(self,nome, sock): # Função para alterar socket de usuário logado
        for i in self.lista_usuario:
            if i.nome == nome:
                i.socket1=sock

def inicializador_de_leiloes(): # Rotina que monitora o início dos leilões
    global controle

    while (1):

        agora = time.time() # aquisição da hora atual em segundos

        #Percorre a lista controle.inicios_de_leilao de 2 em 2 segundos verificando se algum leilão está a menos
        # que 30 minutos para seu início
        for i in controle.inicios_de_leilao:
            # Se faltar menos que 30 minutos para o início do leilão, ele entra no if
            if int(float(i[1])) < agora+30*60:
                cont=0 #Variável para contar a posição dentro da lista
                #Verifica qual o leilão correspondente e armazena em temp2
                for ind in controle.lista_leiloes_futuros:
                    if ind.identificador==i[0]:
                        temp2=ind
                        break
                    cont+=1

                #ferramentas para tratamento leitores-escritores no lance corrente e vencedor corrente

                readcount = 'readcount_lc'+str(temp2.identificador)
                globals()[readcount]=0
                writecount = 'writercount_lc'+str(temp2.identificador)
                globals()[writecount]=0

                rmutex='rmutex_lc' + str(temp2.identificador)
                globals()[rmutex] = threading.BoundedSemaphore()
                wmutex = 'wmutex_lc' + str(temp2.identificador)
                globals()[wmutex] = threading.BoundedSemaphore()
                resource = 'resource_lc' + str(temp2.identificador)
                globals()[resource] = threading.BoundedSemaphore()
                readTry = 'readTry_lc' + str(temp2.identificador)
                globals()[readTry] = threading.BoundedSemaphore()

                prote = 'sem_lp' + str(temp2.identificador)
                globals()[prote]=threading.BoundedSemaphore()

                indice=len(controle.lista_leiloes_correntes)
                controle.lista_leiloes_correntes.append(controle.lista_leiloes_futuros.pop(cont))
                #Troca lista de armazenamento do leilão, passando a usar leiloes_correntes

                #chama thread mata leilão
                matador=threading.Thread(target=mata_leilao, args=(indice,controle.lista_leiloes_correntes[indice].identificador))
                matador.start()

                # chama iniciador
                iniciador = threading.Thread(target=inicio_para_lances, args=(indice, controle.lista_leiloes_correntes[indice].identificador))
                iniciador.start()

                # chama thread escutador
                escutador = threading.Thread(target=escuta_participantes, args=(indice,controle.lista_leiloes_correntes[indice].identificador))
                escutador.start()



                controle.inicios_de_leilao.remove(i) #remove leilão da estrutura de verificação de início

        time.sleep(2)

def mata_leilao(indice,identificador): # Thread que verifica se cada leilão teve lances no período nescessário para ser finalizado
    global controle      # Se não houver, finaliza-se o leilão. Caso haja, calcula-se o tempo até a próxima verificação
    acquire_leitor(identificador)
    temax=controle.lista_leiloes_correntes[indice].t_max
    release_leitor(identificador)

    while 1:


        agora = time.time() # aquisição da hora atual em segundos
        acquire_leitor(identificador)
        soneca=float(controle.lista_leiloes_correntes[indice].hora_ultimo_lance) - float(agora) + float(temax)
        release_leitor(identificador)
        acquire_escritor(identificador)
        if soneca<=0:
            print 'matando leilão'
            controle.lista_leiloes_correntes[indice].flag_de_situacao=2
            release_escritor(identificador)
            acquire_leitor(identificador)
            dono=controle.lista_leiloes_correntes[indice].dono
            vencedor=controle.lista_leiloes_correntes[indice].vencedor_corrente
            nome2=controle.lista_leiloes_correntes[indice].nome
            valor=controle.lista_leiloes_correntes[indice].lance_corrente
            release_leitor(identificador)

            cont1 = 0
            for i in controle.lista_usuario:  # colhendo informações do dono
                if i.nome == dono:
                    endereco_dono = i.endereco
                    telefone_dono = i.telefone
                    email_dono = i.email
                    break
                cont1 += 1

            if str(vencedor) != 'Aguardando o envio':
                cont2=0
                for i in controle.lista_usuario: #colhendo informações do vencedor
                    if i.nome==vencedor:
                        endereco_venc=i.endereco
                        telefone_venc=i.telefone
                        email_venc=i.email
                        #indice_vencedor=i.indice
                        break
                    cont2+=1


                #composição da mensgame contato cliente
                print 'compondo mensagens de contato'
                mens_p_dono = 'Contato_cliente,'+str(identificador)+','+str(valor)+','+str(vencedor)+','+ str(endereco_venc)\
                              +','+ str(telefone_venc)+ ','+ str(email_venc)
                mens_p_vencedor = 'Contato_vendedor,'+ str(identificador)+','+ str(valor)+','+ str(vencedor)+','+ str(endereco_dono)+','+\
                                  str(telefone_dono)+','+ str(email_dono)

                controle.lista_usuario[cont2].mensagens_pendentes.append(mens_p_vencedor)

            else:


                mens_p_dono = 'Leilao_sem_lances,'+str(identificador)
                print '\nNão há vncedor no leilão para receber a mensage de contato do dono\n'
            controle.lista_usuario[cont1].mensagens_pendentes.append(mens_p_dono)
            break
        else:
            release_escritor(identificador)
            time.sleep(soneca)

    print 'mata leilão',identificador,'finalizado'            #mata leilão




def escuta_participantes(indice,identificador):
    #Socket criado para cada leilão, onde a porta é calculada somando-se a porta padrão, 50000, com o identificador do leilão
    #Usado para receber os participantes e estabelecer, através de novos threads, as comunicações síncronas e assíncronas

    global controle
    HOST1 = ''  # Link simbólico representando todas as interfaces disponíveis
    PORT1 = 50000 + int(float(identificador))  # Porta
    com2 = 's' + str(identificador)
    globals()[com2] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket (TCP)
    globals()[com2].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # forçar que o socket desaloque a porta quando fechar o código
    globals()[com2].bind((HOST1, PORT1))  # liga o socket com IP e porta

    while 1:
        globals()[com2].listen(1) #esccuta participantes
        canal_envio, addr2 = globals()[com2].accept() #aceita conecção com cliente

        resp=canal_envio.recv(1024) #recebe posição do cliente na lista de participantes do leilão e seu nome
        resp=resp.split(',')

        posicao_cliente_leilao=int(float(resp[0]))
        nome=resp[1]
        time.sleep(1)
        acquire_escritor(identificador)
        if len(controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao])==3:
            controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao].append(canal_envio)
        else:
            controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][3]=(canal_envio)
        release_escritor(identificador)

        #Thread para a comunicação síncrona
        falador1 = threading.Thread(target=sincrono_lances, args=(canal_envio, indice, identificador, posicao_cliente_leilao, nome))
        falador1.start()

        time.sleep(0.5)

        #Thread para a comunicação asíncrona
        falador2 = threading.Thread(target=assincrono_lances, args=(canal_envio, indice, identificador, posicao_cliente_leilao, nome))
        falador2.start()

def sincrono_lances(canal_envio, indice, identificador, posicao_cliente_leilao, nome):
    global controle

    canal_envio.sendall('Conexão estabelecida para relatórios de leilão,'+str(identificador))


    while 1:
        acquire_leitor(identificador)
        if controle.lista_leiloes_correntes[indice].flag_de_situacao == 2: # Verifica se leilão acabou
            release_leitor(identificador)
            break
        elif controle.lista_leiloes_correntes[indice].flag_de_situacao == 1: # Verifica se leilão está funcionando


            if controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][1]==0: # Verifica se cliente está dentro do leilão
                release_leitor(identificador)
                mensagem(canal_envio, indice, identificador, nome)
                time.sleep(1)
            elif controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][1]==1: # Se cliente online mas fora do leilão, espera

                release_leitor(identificador)
                time.sleep(1)
            else: # Se cliente offline, morre o mensageiro

                release_leitor(identificador)
                break
        else: # se leilão ainda não começou (flag de situação = 0)

            if controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][1]==2: #se cliente saiu do programa

                release_leitor(identificador)
                break
            else:

                release_leitor(identificador)
                time.sleep(1)
    print 'sincrono morreeeeeu'


def assincrono_lances(canal_envio, indice, identificador, posicao_cliente_leilao, nome):
    #Verifica o lance corrente. Se ele for diferente do antigo (ou seja, algum cliente tiver feito um lance), ele envia
    #  a mensagem para os usuários informando que foi feito um novo lance
    acquire_leitor(identificador)
    antigo=controle.lista_leiloes_correntes[indice].lance_corrente
    release_leitor(identificador)
    # flag do participante = 0 : participante dentro do leilão
    # flag do participante = 1 : participante online fora do leilão
    # flag do participante = 2 : participante offline
    prote = 'sem_lp' + str(identificador)
    while 1:
        acquire_leitor(identificador) #trava valor para não haver alteração durante leitura

        if controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][1] == 0:

            # flag de situação = 0: leilão ainda não iniciado
            # flag de situação = 1: leilão em andamento
            # flag de situação = 2: leilão finalizado
            if controle.lista_leiloes_correntes[indice].flag_de_situacao == 0: # verifica se o leilão já começou
                release_leitor(identificador) # leitura terminada, libera para escrita
                time.sleep(1)
            elif controle.lista_leiloes_correntes[indice].flag_de_situacao == 1: # verifica se o leilão já começou:
                novo = controle.lista_leiloes_correntes[indice].lance_corrente
                release_leitor(identificador)  # leitura terminada, libera para escrita (novos lances)
                if novo!=antigo: #testa se houve lance
                    mensagem(canal_envio, indice, identificador, nome)
                    antigo=novo
                time.sleep(0.2)

            elif controle.lista_leiloes_correntes[indice].flag_de_situacao == 2:
                print "mensagens finais"

                mess= 'Fim_leilao,'+str(identificador)+','+str(controle.lista_leiloes_correntes[indice].lance_corrente)+\
                      ','+str(controle.lista_leiloes_correntes[indice].vencedor_corrente)
                canal_envio.sendall(mess)

                release_leitor(identificador)
                break  # Sai do while 1 para morrer


        elif controle.lista_leiloes_correntes[indice].participantes[posicao_cliente_leilao][1] == 1:

            release_leitor(identificador)
            time.sleep(1)
            pass
        else: # flag=2, matar comunicações com cliente sobre este leilão
            release_leitor(identificador)
            break
    time.sleep(0.5)
    canal_envio.sendall('Morraaaa')
    print "assíncrono morreeeu"

def mensagem(canal_envio, indice, identificador, nome):
    acquire_leitor(identificador)
    cont=0
    for i in controle.lista_leiloes_correntes[indice].participantes: # contagem de participantes do leilão
        if i[1]==0:
            cont+=1
    mensagem = 'Lance,' + str(identificador) + ',' \
               + controle.lista_leiloes_correntes[indice].vencedor_corrente + ',' \
               + str(controle.lista_leiloes_correntes[indice].lance_corrente) + ',' \
               + str(cont) + ',' \
               + str(controle.lista_leiloes_correntes[indice].conta_lances)
    release_leitor(identificador)
    canal_envio.sendall(mensagem)

def inicio_para_lances(indice, identificador):
    global controle  # Se não houver, finaliza-se o leilão. Caso haja, calcula-se o tempo até a próxima verificação

    agora = time.time()  # aquisição da hora atual em segundos
    acquire_leitor(identificador)
    soneca = float(controle.lista_leiloes_correntes[indice].hora_leilao) - float(agora)
    release_leitor(identificador)
    time.sleep(soneca)
    acquire_escritor(identificador)
    controle.lista_leiloes_correntes[indice].flag_de_situacao=1
    release_escritor(identificador)
    print 'leilão '+str(identificador)+'aberto pra lances'


def teste_de_data(dia,mes,ano,hora,minuto,segundo,flag): # função pra testar se a hora e data do leilão é no futuro
    hora_leilao = str(dia) + '/' + str(mes) + '/' + str(ano) + ' ' + str(hora) + ':' + str(minuto) \
                  + ':' + str(segundo)  # para verificação se data é no futuro
    hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
    hora_leilao = time.mktime(hora_leilao.timetuple())
    agora = time.time()

    if flag != 0:
        agora = agora + 30*60

    if agora < hora_leilao:
        return 1
    else:
        return 0

def listar_leiloes(conn,lista):
    conn.sendall(str(len(lista)))
    time.sleep(0.3)
    for i in lista:
        lista1 = ('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}'.format('Listagem', str(i.nome), str(i.identificador),
        str(i.descricao), str(i.lance_minimo),str(i.dia), str(i.mes), str(i.ano), str(i.hora),str(i.minuto), str(i.segundo),
        str(i.t_max), str(i.dono)))
        conn.sendall(lista1)
        time.sleep(0.1)

def cria_arquivos_leilao():
    try:
        f = open('leiloes_futuros.txt')  # Abre o arquivo leiloes_futuros.txt. Se não tiver, ele acusa erro e cria um
        f.close()

    except IOError:
        f = open('leiloes_futuros.txt','w')
        f.close()
    try:
        f = open('numero_de_leiloes_cadastrados.txt')  # Abre o arquivo numero_de_leiloes_cadastrados.txt. Se não tiver, ele acusa erro e cria um
        f.close()

    except IOError:
        f = open('numero_de_leiloes_cadastrados.txt','w')
        f.write('0')
        f.close()

    try:
        f = open('numero_de_clientes_cadastrados.txt')  # Abre o arquivo numero_de_leiloes_cadastrados.txt. Se não tiver, ele acusa erro e cria um
        f.close()

    except IOError:
        f = open('numero_de_clientes_cadastrados.txt','w')
        f.write('0')
        f.close()


def mesageiro_de_finais(conn3, name, logado):
    morte = 'morte_' + str(logado)
    for i in controle.lista_usuario:  # Verificação de mensagen pendentes no login
        if i.nome == name:
            while 1:
                if globals()[morte]==0:
                    #aqui tem que entrar proteção pra controle
                    if len(i.mensagens_pendentes) != 0:  # Existem mensagens a serem enviadas

                        conn3.sendall(str(i.mensagens_pendentes.pop(0)))
                        print 'enviando fim pro thread novo'
                    time.sleep(1)
                else:
                    conn3.sendall('morraa')
                    print '\Morre o enviador de finais'
                    break


#Servidor Thread
def servidor(conn,addr):
    print 'Conectado por', addr, "\n"
    global controle
    name = ' '
    estado=0 # Indicador de que existe algúem logado
    while 1: # Responsável pelas opções do "switch1"
        resp = conn.recv(1024)  # Cliente dizendo se quer cadastrar ou fazer login, com seus respectivos parâmetros
        if not resp: break #Sai do loop caso valor seja nulo ou 0
        a = resp.split(",") #Informações do usuário separados na lista 'a'
        #print "Recebi"
        if a[0] == 'Adiciona_usuario':
            #print "entrei no if"
            while 1: #Fica no loop para caso o nome seja repetido, ele tentar registrar novamente
                flag = controle.checar_nome_existente(a[1],0,a[5]) #Checar se o nome já foi cadastrado
                #print "Chequei nome"
                if flag == 1: #Se o nome for repetido, ele manda uma resposta ao cliente
                    conn.sendall('not_ok')
                    print
                else:
                    arquivo2 = open('numero_de_clientes_cadastrados.txt', 'r')
                    num_clientes = 0
                    for lin in arquivo2:
                        num_clientes = lin
                        #print 'Número de leilões cadastrados absorvidos ' + str(num_clientes) + '\n'
                    arquivo2.close()
                    num_clientes=int(float(num_clientes))+1
                    arquivo2 = open('numero_de_clientes_cadastrados.txt', 'w')  # trocando
                    arquivo2.write(str(num_clientes))
                    arquivo2.close()
                    nome = user(a[1],a[2],a[3],a[4],a[5],str(addr),num_clientes) # crio objeto 'nome' da classe usuário
                    name = a[1] # armazenamento do nome do cliente logado para utilização na criação de leilão
                    print "criei objeto da classe usuário"
                    logado=controle.adc_usuario(nome) #adiciona usuário ao .txt e retorna o índice do usuário
                    controle.onlines.append(name) #Adiciona o usuário à lista dos usuários logados
                    print "Arquivei usuario"
                    conn.sendall('ok')
                    time.sleep(0.3)
                    conn.sendall(str(logado))
                    estado = 1  # alteração do servidor para switch 2 ao fim do while(1) (logado)

                    # socket para recebimento de mensagens d fim de leilão
                    HOST3 = ''  # Link simbólico representando todas as interfaces disponíveis
                    PORT3 = 60000 + logado  # Porta
                    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket (TCP)
                    s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                  1)  # forçar que o socket desaloque a porta quando fechar o código
                    s3.bind((HOST3, PORT3))  # liga o socket com IP e porta
                    s3.listen(1)
                    conn3, addr3 = s3.accept()  # Aceita uma conexão
                    morte='morte_'+str(logado)
                    globals()[morte]=0
                    envia_finais = threading.Thread(target=mesageiro_de_finais, args=(conn3, name, logado))
                    envia_finais.start()

                    break

        elif a[0] == 'Faz_login':
            while 1: #Fica no loop para caso a ele erre alguma coisa, tentar novamente
            #Se o nome que ele digitou for igual ao nome e a senha
            # forem iguais as que tenho no regsitro, ele faz o login
                try:
                    k1=controle.checar_nome_existente(a[1], 1, a[2]) # Verificação se nome existe
                    if (k1 == 1):

                        logado = controle.retorna_usuario(a[1], addr)
                        print 'Usuário '+str(logado.nome)+' de índice '+str(logado.indice.strip())+' logado com ip e porta '+str(logado.socket1)+'\n'
                        name = logado.nome # armazenamento do nome do cliente logado para utilização na criação de leilão
                        logado=logado.indice
                        controle.onlines.append(name) # guardamos o identificador do cliente

                        conn.sendall('ok')
                        time.sleep(0.3)
                        conn.sendall(str(logado))
                        estado = 1 # alteração do servidor para switch 2 ao fim do while(1) (logado)


                        #socket para recebimento de mensagens d fim de leilão
                        HOST3 = ''  # Link simbólico representando todas as interfaces disponíveis
                        PORT3 = 60000 + int(logado )# Porta
                        s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket (TCP)
                        s3.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                                     1)  # forçar que o socket desaloque a porta quando fechar o código
                        s3.bind((HOST3, PORT3))  # liga o socket com IP e porta
                        s3.listen(1)
                        conn3, addr3 = s3.accept()  # Aceita uma conexão

                        for i in controle.lista_usuario: # Verificação de mensagen pendentes no login
                            if i.nome == name:
                                if len(i.mensagens_pendentes) != 0: #Existem mensagens a serem enviadas
                                    time.sleep(0.5)
                                    for ii in range(len(i.mensagens_pendentes)):
                                        conn3.sendall(str(i.mensagens_pendentes.pop(0)))

                        morte = 'morte_' + str(logado)
                        globals()[morte] = 0
                        envia_finais = threading.Thread(target=mesageiro_de_finais, args=(conn3,name, logado))
                        envia_finais.start()



                    else:
                        conn.sendall('not_ok')
                except KeyError:
                    print ('Usuário não existe')
                    conn.sendall('not_ok')
                    # Perguntar se mando essa mensagem para o cliente ou se é só para mandar o not_ok
                break  # sai do 'Faz_login' loop mas continua no loop princpal
        elif a[0] == 'Lista_leiloes':
            # conn.sendall(listar_leiloes(0))
            print 'Listando leilões para anônimo\n'
            listar_leiloes(conn,controle.lista_leiloes_correntes)
            listar_leiloes(conn,controle.lista_leiloes_futuros)



        while estado == 1: # Switch 2
            print 'switch2\n'
            resp=conn.recv(1024)
            b=resp.split(',')

            if b[0]=='Lanca_produto': # lançamento de novo produto
                print 'Trecho de lançamento de produto\n'
                #atrib = [0] * (len(b))  #  lista vazia para armazenamento de

                for i in range(3,10):  # Transforma strings de saída da mensagem em floats
                    b[i] = int(float(b[i]))

                # Verifica se a data e hora de início de leilão não expiraram

                if teste_de_data(b[4], b[5], b[6], b[7], b[8], b[9],0) == 1:
                    arquivo = open('numero_de_leiloes_cadastrados.txt', 'r')
                    num_leiloes = 0
                    for lin in arquivo:
                        num_leiloes=lin
                        #print 'Número de leilões cadastrados absorvidos '+str(num_leiloes)+'\n'
                    arquivo.close()
                    num_leiloes=int(num_leiloes)+1
                    arquivo = open('numero_de_leiloes_cadastrados.txt','w')  # trocando
                    arquivo.write(str(num_leiloes))
                    arquivo.close()
                    leilaao = leilao( b[1], b[2], b[3], b[4],b[5],b[6],b[7],b[8],b[9],b[10],name)
                    leilaao.identificador=num_leiloes
                    controle.lista_leiloes_futuros.append(leilaao)
                    leilaao.arquivar_leilao_futuro()
                    hora_leilao = str(b[4]) + '/' + str(b[5]) + '/' + str(b[6]) + ' ' + str(b[7]) + ':' + str(b[8]) \
                                  + ':' + str(b[9])  # para verificação se data é no futuro
                    hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
                    hora_leilao = time.mktime(hora_leilao.timetuple())
                    controle.inicios_de_leilao.append([leilaao.identificador, hora_leilao]) #Adiciona o identificador do leilão e
                    #  a hora em que ele começa
                    conn.sendall('ok')
                    print 'Leilão criado com sucesso\n'
                else:
                    # aviso de que algum leilão perdeu a data de inicio com servidor off line
                    print '\nLeilão de ' + str(b[1]) + ' marcado para antes de agora.\n'
                    conn.sendall('not_ok')

            elif b[0] == 'Lista_leiloes':
                print 'Listando leilões para usuário\n'
                #conn.sendall(listar_leiloes(1))
                listar_leiloes(conn, controle.lista_leiloes_correntes)
                listar_leiloes(conn, controle.lista_leiloes_futuros)

            elif b[0] == 'Apaga_usuario':
                print 'Cliente resolveu apagar usuario'
                arq = open('clientes.txt','w')  # apagando txt de usuários
                arq.close()  #
                temp=open('clientes.txt','a')
                for ind in controle.lista_usuario:
                    if ind.indice!=logado:
                        print ind.nome+' rearquivado'
                        temp.write(ind.nome + ',' + ind.telefone + ',' + ind.endereco + ',' + ind.email + ',' + ind.senha+','+ind.socket1+','+str(ind.indice))
                    else:
                        flag= ind
                        print ind.nome+' removido'
                controle.lista_usuario.remove(flag)
                temp.close()
                estado=0
                conn.sendall('ok')

            elif b[0]=='Entrar_leilao':

                flag3=0
                for i in controle.lista_leiloes_correntes: #corre todos os leilões em andamento
                    acquire_leitor(i.identificador)
                    if b[1] == str(i.identificador): # executado quando o leilão pedido está em andamento
                        flag3 = 1
                        if i.dono!=name:


                            flag4=0
                            cont2=0
                            for ii in i.participantes: # corre clientes do leilão
                                if float(logado) == float(ii[0]): # verifica se cliente já esteve neste leilão
                                    if ii[1]==1: # Verifica se os threads mensageiros ainda existem
                                        print 'voltei'
                                        flag4 = 1 # Executado quando os threads não devem ser criados novamente
                                        break
                                    elif ii[1]==0: #cliente ainda participa do leilão
                                        flag4 = 2
                                        break
                                    else : #cleinte sai do sistema matando todos os threads mensageiros depois de entrar no leilão
                                        flag4 = 3
                                        break
                                cont2+=1
                            release_leitor(i.identificador)
                            print flag4
                            if flag4==0:
                                print 'tentativa de primeira entrada no leilão'
                                conn.sendall('ok')
                                time.sleep(0.4)
                                acquire_escritor(i.identificador)
                                i.participantes.append([int(float(logado)), 0, 0])
                                conn.sendall(str(len(i.participantes)-1))
                                print i.participantes
                                release_escritor(i.identificador)
                                break
                            elif flag4==1:
                                print 'tentativa de reconexão'
                                acquire_escritor(i.identificador)
                                i.participantes[cont2][1]=0 # Reestabelece o status online para o cliente no leilão
                                release_escritor(i.identificador)
                                conn.sendall('ok') # relogin efetuado com sucesso
                                break
                            elif flag4==2:
                                print 'negado pois já está no leilão'
                                conn.sendall('not_ok') # mensagem de que cliente não deve
                                                       #  ser incluido mais de uma vez no mesmo leilão
                                break
                            else:
                                print 'cliente retornando após ter deslogado'
                                conn.sendall('ok')
                                time.sleep(0.4)
                                acquire_escritor(i.identificador)
                                i.participantes[cont2][1]=0
                                conn.sendall(str(cont2))
                                print i.participantes
                                release_escritor(i.identificador)
                                break
                        else:
                            print '\nDono do leilão não deve concorrer como comprador'
                            release_leitor(i.identificador)
                            conn.sendall('not_ok')
                            break

                if flag3==0:
                    print 'leilão não existente'
                    conn.sendall('not_ok')


            elif b[0] == 'Sair':
                estado=0
                for i in controle.lista_leiloes_correntes:
                    for ii in i.participantes:
                        if ii[0]==int(float(logado)):
                            acquire_escritor(i.identificador)
                            ii[1]=2
                            release_escritor(i.identificador)

                            break
                print 'Cliente '+str(logado)+' resolveu sair'
                controle.onlines.remove(name)
                morte = 'morte_' + str(logado)
                globals()[morte] = 1 # variável compartilhada para matar thread de fim de leilão
                conn.sendall('ok')

            elif b[0]=='Sair_leilao':
                for i in controle.lista_leiloes_correntes:
                    print b[1]
                    print i.identificador
                    if int(i.identificador)==int(float(b[1])):
                        acquire_escritor(i.identificador)
                        i.participantes[int(float(b[2]))][1]=1
                        print 'Usuário '+str(logado.strip())+' saiu do leilão '+ str(i.identificador)
                        release_escritor(i.identificador)
                        conn.sendall('ok')
                        break


            elif b[0] == 'Enviar lance':
                b[2]=float(b[2])
                indice=0
                flaag=0
                for i in controle.lista_leiloes_correntes:
                    if b[1] == str(i.identificador):
                        flaag=1
                        identificador=i.identificador
                        break
                    indice=+1
                print 'indice', indice
                
                if flaag == 0:
                    #Se o identicador enviado não é válido, envia not_ok_1
                    conn.sendall('not_ok,1')
                else:
                    acquire_leitor(identificador)
                    if controle.lista_leiloes_correntes[indice].flag_de_situacao==0:
                        release_leitor(identificador)
                        # Se o leilão ainda não tiver começado
                        conn.sendall('not_ok,3')
                    elif b[2] <= controle.lista_leiloes_correntes[indice].lance_corrente:
                        release_leitor(identificador)
                        #Se o valor do lance for menor que o lance corrente envia not_ok_2
                        conn.sendall('not_ok,2')
                    else:
                        # se está tudo ok
                        release_leitor(identificador)

                        acquire_escritor(identificador)
                        print 'Nome logado',name
                        print 'Vencedor_corrente', controle.lista_leiloes_correntes[indice].vencedor_corrente
                        controle.lista_leiloes_correntes[indice].vencedor_corrente = name #nome do usuário logado
                        print 'Vencedor_corrente',controle.lista_leiloes_correntes[indice].vencedor_corrente
                        print 'Valor recebido',b[2]
                        controle.lista_leiloes_correntes[indice].lance_corrente = float(b[2]) #Recebe o valor atualizado
                        print 'Valor_corrente', controle.lista_leiloes_correntes[indice].lance_corrente
                        controle.lista_leiloes_correntes[indice].conta_lances+=1
                        controle.lista_leiloes_correntes[indice].hora_ultimo_lance=time.time()
                        release_escritor(controle.lista_leiloes_correntes[indice].identificador)

                        conn.sendall('ok')




#Uso de semáforo para fazer o controle dos leitores-escritores, com prioridade para os escritores.
#O identicador é relativo a cada leilão

def acquire_leitor(identificador):
    readcount = 'readcount_lc' + str(identificador)
    rmutex = 'rmutex_lc' + str(identificador)
    resource = 'resource_lc' + str(identificador)
    readTry = 'readTry_lc' + str(identificador)

    globals()[readTry].acquire() # Indica que o leitor que ler
    globals()[rmutex].acquire() # Bloqueia seção para evitar inconsistência nas variáveis de controle
    globals()[readcount]+=1 # Incrementa o contador de leitores
    if globals()[readcount] == 1: # Checa se você é o primeiro leitor
        globals()[resource].acquire() # Se for o primeiro leitor, bloqueia escritores
    globals()[rmutex].release() # Libera a seção de entrada para outros leitores
    globals()[readTry].release() # Indica que você acabou de acessar o recurso


def release_leitor(identificador):
    readcount = 'readcount_lc' + str(identificador)
    rmutex = 'rmutex_lc' + str(identificador)
    resource = 'resource_lc' + str(identificador)

    globals()[rmutex].acquire() #Reserva a seção de saída - evita condição de corrida com os leitores
    globals()[readcount]-=1 #Indica que você está saindo
    if globals()[readcount] == 0: #Checa se você é o último leitor saindo
        globals()[resource].release() #Śe for o último, você deve liberar o recurso reservado
    globals()[rmutex].release() #Libera a seção de saída para outro leitor


def acquire_escritor(identificador):
    writecount = 'writercount_lc' + str(identificador)
    rmutex = 'rmutex_lc' + str(identificador)
    resource = 'resource_lc' + str(identificador)
    readTry = 'readTry_lc' + str(identificador)

    globals()[rmutex].acquire() #Reserva a seção de entrada para os escritores - evita condição de corrida
    globals()[writecount]+=1 #Reporta você como um escritor entrando
    if globals()[writecount] == 1: #Checa se você é o primeiro escritor
        globals()[readTry].acquire() #Se você é o primeiro, então deve bloquear os leitores. Evita que eles entrem  na Seção Crítica
    globals()[rmutex].release() #Libera a seção de entrada
    globals()[resource].acquire() #Reserca o recurso para você mesmo. Evita que outros escritores editem o recurso compartilhado
    # de modo simultâneo


def release_escritor(identificador):
    writecount = 'writercount_lc' + str(identificador)
    wmutex = 'wmutex_lc' + str(identificador)
    resource = 'resource_lc' + str(identificador)
    readTry = 'readTry_lc' + str(identificador)

    globals()[resource].release() #Libera arquivo
    globals()[wmutex].acquire() #Reserva a seção crítica
    globals()[writecount]-=1 #Indica que você está saindo
    if globals()[writecount] == 0: #Checa se você é o último escritor
        globals()[readTry].release() #Se for o último, então você deve liberar o acesso aos leitores.
        # Permite que eles entrem na seção crítica
    globals()[wmutex].release() #Libera a seção crítica

if __name__ == '__main__':  ###Programa principal

    HOST = ''                 # Link simbólico representando todas as interfaces disponíveis
    PORT = 50000              # Porta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket (TCP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código
    s.bind((HOST, PORT)) #liga o socket com IP e porta

    print "---------Servidor funcionado---------"
    print "Esperando pelos clientes\n"
    controle = controle_geral()  # carrega os usuarios que estavam no clientes.txt
    cria_arquivos_leilao()
    ini = threading.Thread(target=inicializador_de_leiloes, args=())
    ini.start()
    clientes=0
    #logado=None
    while 1:
        s.listen(1)
        conn, addr = s.accept()  # Aceita uma conexão
        clientes += 1
        print "\nNúmero de clientes conectados", clientes
        t = threading.Thread(target=servidor, args=(conn,addr))
        t.start()
