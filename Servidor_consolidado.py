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

    # Contrutor de novos leilões
    def __init__(self,nome, descricao,lance_minimo, dia, mes, ano, hora, minuto, segundo, t_max, dono):
        self.nome=nome
        self.descricao=descricao
        self.lance_minimo=lance_minimo
        self.lance_corrente=lance_minimo # protegida
        self.vencedor_corrente='Aguardando o envio' # protegida

        hora_leilao = str(dia) + '/' + str(mes) + '/' + str(ano) + ' ' + str(hora) + ':' + str(minuto) \
                      + ':' + str(segundo)  # para verificação se data é no futuro
        hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
        hora_leilao = time.mktime(hora_leilao.timetuple())

        self.conta_lances=0
        self.hora_ultimo_lance=hora_leilao # protegida
        self.lance_vencedor=lance_minimo
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
        # Mudança para estrutura mais simples
        """
        temp = datetime.datetime.now()
        agora = str(temp.day) + '/' + str(temp.month) + '/' + str(temp.year) + ' ' + str(temp.hour) + ':' + str(
            temp.minute) + ':' + str(temp.second)
        agora = datetime.datetime.strptime(agora, "%d/%m/%Y %H:%M:%S")
        agora = time.mktime(agora.timetuple())
        """
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
                    cont=cont+1

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
                matador=threading.Thread(target=mata_leilao, args=(indice,))
                matador.start()

                # chama thread escutador
                escutador = threading.Thread(target=escuta_participantes, args=(indice,))
                escutador.start()

                controle.inicios_de_leilao.remove(i) #remove leilão da estrutura de verificação de início

        time.sleep(2)

def mata_leilao(indice): # Thread que verifica se cada leilão teve lances no período nescessário para ser finalizado
    global controle      # Se não houver, finaliza-se o leilão. Caso haja, calcula-se o tempo até a próxima verificação
    temax=controle.lista_leiloes_correntes[indice].t_max

    while 1:
        # Mudança para estrutura mais simples
        """
        temp = datetime.datetime.now()
        agora = str(temp.day) + '/' + str(temp.month) + '/' + str(temp.year) + ' ' + str(temp.hour) + ':' + str(
            temp.minute) + ':' + str(temp.second)
        agora = datetime.datetime.strptime(agora, "%d/%m/%Y %H:%M:%S")
        agora = time.mktime(agora.timetuple())
        """
        agora = time.time() # aquisição da hora atual em segundos

        soneca=float(controle.lista_leiloes_correntes[indice].hora_ultimo_lance) - float(agora) + float(temax)
        antigo_lance=controle.lista_leiloes_correntes[indice].lance_corrente
        time.sleep(soneca)
        if controle.lista_leiloes_correntes[indice].lance_corrente==antigo_lance:
            #mata leilão
            print 'matei leilão'
            time.sleep(5)

def escuta_participantes(indice):
    #Socket criado para cada leilão, onde a porta é calculada somando-se a porta padrão, 50000, com o identificador do leilão
    #Usado para receber os participantes e estabelecer, através de novos threads, as comunicações síncronas e assíncronas

    global controle
    HOST1 = ''  # Link simbólico representando todas as interfaces disponíveis
    PORT1 = 50000 + int(float(controle.lista_leiloes_correntes[indice].identificador))  # Porta
    com2 = 's' + str(controle.lista_leiloes_correntes[indice].identificador)
    globals()[com2] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4,tipo de socket (TCP)
    globals()[com2].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  # forçar que o socket desaloque a porta quando fechar o código
    globals()[com2].bind((HOST1, PORT1))  # liga o socket com IP e porta

    while 1:
        globals()[com2].listen(1)
        canal_envio, addr2 = globals()[com2].accept()

        #Thread para a comunicação síncrona
        falador1 = threading.Thread(target=sincrono_lances, args=(canal_envio, indice))
        falador1.start()

        #Thread para a comunicação asíncrona
        falador2 = threading.Thread(target=assincrono_lances, args=(canal_envio, indice))
        falador2.start()

def sincrono_lances(canal_envio,indice):
    global controle

    canal_envio.sendall('\nConexão estabelecida para relatórios de leilão\n')

    while 1:
        time.sleep(1)
        mensagem(canal_envio,indice)


def assincrono_lances(canal_envio, indice):
    #Verifica o lance corrente. Se ele for diferente do antigo (ou seja, algum cliente tiver feito um lance), ele envia
    #  a mensagem para os usuários informando que foi feito um novo lance
    acquire_leitor(controle.lista_leiloes_correntes[indice].identificador)
    antigo=controle.lista_leiloes_correntes[indice].lance_corrente
    release_leitor(controle.lista_leiloes_correntes[indice].identificador)
    while 1:
        time.sleep(0.2)
        acquire_leitor(controle.lista_leiloes_correntes[indice].identificador)
        novo = controle.lista_leiloes_correntes[indice].lance_corrente
        release_leitor(controle.lista_leiloes_correntes[indice].identificador)
        if novo!=antigo:
            mensagem(canal_envio,indice)

def mensagem(canal_envio,indice):
    acquire_leitor(controle.lista_leiloes_correntes[indice].identificador)
    mensagem = 'Leilão número ' + str(controle.lista_leiloes_correntes[indice].identificador) + '\n' \
               + 'Vencedor até o momento: ' + controle.lista_leiloes_correntes[indice].vencedor_corrente + '\n' \
               + 'Lance vencedor até o momento: R$' + str(controle.lista_leiloes_correntes[indice].lance_corrente) + '\n' \
               + 'Número de usuários participantes: ' + str(
        len(controle.lista_leiloes_correntes[indice].participantes)) + '\n' \
               + 'Número de lances já efetuados: ' + str(controle.lista_leiloes_correntes[indice].conta_lances) + '\n'
    release_leitor(controle.lista_leiloes_correntes[indice].identificador)
    canal_envio.sendall(mensagem)



def teste_de_data(dia,mes,ano,hora,minuto,segundo,flag): # função pra testar se a hora e data do leilão é no futuro

    hora_leilao = str(dia) + '/' + str(mes) + '/' + str(ano) + ' ' + str(hora) + ':' + str(minuto) \
                  + ':' + str(segundo)  # para verificação se data é no futuro
    hora_leilao = datetime.datetime.strptime(hora_leilao, "%d/%m/%Y %H:%M:%S")
    hora_leilao = time.mktime(hora_leilao.timetuple())

    #Mudança para estrutura mais simples
    """
    temp = datetime.datetime.now()
    agora = str(temp.day) + '/' + str(temp.month) + '/' + str(temp.year) + ' ' + str(temp.hour) + ':' + str(
        temp.minute) + ':' + str(temp.second)
    agora = datetime.datetime.strptime(agora, "%d/%m/%Y %H:%M:%S")
    agora = time.mktime(agora.timetuple())
    """
    agora = time.time()

    if flag != 0:
        agora = agora + 30*60

    if agora < hora_leilao:
        return 1
    else:
        return 0


def listar_leiloes(valor):
    if valor == 1:
        lista1 = '\nLeilões em que você está apto a participar:\n'
        lista2 = "\nLeilões futuros com mais de 30 minutos para iniciar:\n"
    else:
        lista1 = '\nLeilões armazenados:\n'
        lista2 = ""

    for i in controle.lista_leiloes_correntes:

        lista1 = ( lista1 + '\nNome do produto: ' + str(i.nome) + '\nÍndice: ' + str(i.identificador) + '\nDescrição do produto: ' + str(i.descricao) +\
            '\nLance mínimo: R$' + str(i.lance_minimo) + '\nDia e hora do leilão: ' + str(i.dia) + '/' +\
            str(i.mes) + '/' + str(i.ano) + ' as ' + str(i.hora) + ':' + str(i.minuto) + ':' + str(\
            i.segundo) +'\nO tempo máximo entre lances é de: ' + str(i.t_max) + ' segundos'+\
            '\nO leilao pertence a: ' + str(i.dono) + '\n')

    for i in controle.lista_leiloes_futuros:
        lista2 = (lista2 + '\nNome do produto: ' + str(i.nome) + '\nÍndice: ' + str(i.identificador) + '\nDescrição do produto: ' + str(i.descricao) + \
            '\nLance mínimo: R$' + str(i.lance_minimo) + '\nDia e hora do leilão: ' + str(i.dia) + '/' + \
            str(i.mes) + '/' + str(i.ano) + ' as ' + str(i.hora) + ':' + str(i.minuto) + ':' + str( \
            i.segundo) + '\nO tempo máximo entre lances é de: ' + str(i.t_max) + ' segundos' + \
            '\nO leilao pertence a: ' + str(i.dono) + '\n')
    lista = lista1+lista2
    return lista

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

#Servidor Thread
def servidor(conn,addr):
    print 'Conectado por', addr, "\n"
    global controle
    name = ' '
    estado=0 # Indicador de que existe algúem logado
    cria_arquivos_leilao()
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
                    nome = user(a[1],a[2],a[3],a[4],a[5],str(addr),len(controle.lista_usuario)+1) # crio objeto 'nome' da classe usuário
                    name = a[1] # armazenamento do nome do cliente logado para utilização na criação de leilão
                    print "criei objeto da classe usuário"
                    logado=controle.adc_usuario(nome) #adiciona usuário ao .txt e retorna o índice do usuário
                    controle.onlines.append(logado) #Adiciona o usuário à lista dos usuários logados
                    print "Arquivei usuario"
                    conn.sendall('ok')
                    estado = 1 # # alteração do servidor para switch 2 ao fim do while(1) (logado)
                    break

        elif a[0] == 'Faz_login':
            while 1: #Fica no loop para caso a ele erre alguma coisa, tentar novamente
            #Se o nome que ele digitou for igual ao nome e a senha
            # forem iguais as que tenho no regsitro, ele faz o login
            ## print "Entrei login"
            #nome1 = globals()[a[1]].nome #Como fazer a comparação direto?
                try:
                    k1=controle.checar_nome_existente(a[1],1,a[2]) # Verificação se nome existe
                    if (k1 == 1):

                        logado = controle.retorna_usuario(a[1],addr)
                        print 'Usuário '+str(logado.nome)+' de índice '+str(logado.indice.strip())+' logado com ip e porta '+str(logado.socket1)+'\n'
                        name = logado.nome # armazenamento do nome do cliente logado para utilização na criação de leilão
                        logado=logado.indice
                        controle.onlines.append(logado) #acréscimo do cliente a variável de controle dos usuários logados

                        conn.sendall('ok')
                        estado = 1 # alteração do servidor para switch 2 ao fim do while(1) (logado)
                    else:
                        conn.sendall('not_ok')
                except KeyError:
                    print ('Usuário não existe')
                    conn.sendall('not_ok')
                    # Perguntar se mando essa mensagem para o cliente ou se é só para mandar o not_ok
                break  # sai do 'Faz_login' loop mas continua no loop princpal
        elif a[0] == 'Lista_leiloes':
            print 'Listando leilões para anônimo\n'
            conn.sendall(listar_leiloes(0))



        elif a[0] == 'Desligar':
                                                             ##
            arquivo = open('leiloes_futuros.txt', 'w') # apagando conteúdo do txt dos leiloes não terminados
            arquivo.close()                                   #
                                                             ##

            arquivo = open('leiloes_futuros.txt', 'w') # atualizando txt com valor dos leilões ainda não terminados
            cont=1
            for i in controle.lista_leiloes_correntes:
                if teste_de_data(i.dia,i.mes,i.ano,i.h,i.minuto,i.segundo,0)==1:
                    arquivo.write(i.nome + ',' + i.descricao + ',' + str(i.lance_minimo) + ',' + str(i.dia) + ',' + str(i.mes) + ',' + str(i.ano) + ',' + str(i.ano) + ',' + str(i.hora) + ',' + str(i.minuto) + ',' + str(i.segundo) + ',' + str(i.t_max) + ',' + i.dono + +','+str(cont)+'\n')
                    cont=cont+1
                    # aqui vai comando pra matar thread

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
                        print 'Número de leilões cadastrados absorvidos '+str(num_leiloes)+'\n'
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
                    print controle.inicios_de_leilao
                    conn.sendall('ok')
                    print 'Leilão criado com sucesso\n'
                else:
                    # aviso de que algum leilão perdeu a data de inicio com servidor off line
                    print '\nLeilão de número ' + str(b[1]) + ' marcado para antes de agora.\n'
                    conn.sendall('not_ok')

            elif b[0] == 'Lista_leiloes':
                print 'Listando leilões para usuário\n'
                conn.sendall(listar_leiloes(1))

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
                cont=0
                for i in controle.lista_leiloes_correntes:

                    if b[1] == str(i.identificador):
                        b[1] = int(float(b[1]))
                        conn.sendall('ok')
                        flag3 = 1
                        time.sleep(0.4)
                        prote='sem_lp'+str(i.identificador)
                        globals()[prote].acquire()
                        i.participantes.append([int(float(logado)), 0])
                        print i.participantes
                        globals()[prote].release()
                        break
                    cont=cont+1

                if flag3==0:
                    conn.sendall('not_ok')

            elif b[0] == 'Sair':
                estado=0
                for i in controle.lista_leiloes_correntes:
                    for ii in i.participantes:
                        if ii[1]==int(float(logado)):
                            prote = 'sem_lp' + str(i.identificador)
                            globals()[prote].acquire()
                            i.remov(ii)
                            globals()[prote].release()
                print 'Cliente resolveu sair'
                conn.sendall('ok')

            elif b[0] == 'Enviar lance':
                indice=0
                flaag=0
                for i in controle.lista_leiloes_correntes:
                    if b[1] == str(i.identificador):
                        flaag=1
                        break
                    indice=+1
                print 'indice', indice
                
                if flaag == 0:
                    #Se o identicador enviado não é válido, envia not_ok_1
                    conn.sendall('not_ok,1')
                else:
                    acquire_leitor(controle.lista_leiloes_correntes[indice].identificador)
                    if float(b[2]) <= float(controle.lista_leiloes_correntes[indice].lance_corrente):
                        release_leitor(controle.lista_leiloes_correntes[indice].identificador)
                        #Se o valor do lance for menor que o lance corrente envia not_ok_2
                        conn.sendall('not_ok,2')
                    else:
                        release_leitor(controle.lista_leiloes_correntes[indice].identificador)

                        acquire_escritor(controle.lista_leiloes_correntes[indice].identificador)
                        print 'Nome logado',name
                        print 'Vencedor_corrente', controle.lista_leiloes_correntes[indice].vencedor_corrente
                        controle.lista_leiloes_correntes[indice].vencedor_corrente = name #nome do usuário logado
                        print 'Vencedor_corrente',controle.lista_leiloes_correntes[indice].vencedor_corrente
                        print 'Valor recebido',b[2]
                        controle.lista_leiloes_correntes[indice].lance_corrente = float(b[2]) #Recebe o valor atualizado
                        print 'Valor_corrente', controle.lista_leiloes_correntes[indice].lance_corrente
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
