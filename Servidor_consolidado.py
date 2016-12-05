#!/usr/bin/env python
# encoding: utf-8

import socket, os, threading, datetime, time

class leilao: # Classe dos leilões
    identificador=0
    nome=' '
    descricao=' '
    lance_minimo=0
    lance_corrente=0
    lance_vencedor=0
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

    # Contrutor de novos leilões
    def __init__(self,nome, descricao,lance_minimo, dia, mes, ano, hora, minuto, segundo, t_max, dono):
        self.nome=nome
        self.descricao=descricao
        self.lance_minimo=lance_minimo
        self.lance_corrente=lance_minimo
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

        # Método para salvar leilões nos arquivos txt
    def arquivar_leilao(self):
        f = open('leiloes_nao_terminados.txt','a') # Escreve as linhas a partir da útlima linha escrita
        f.write(str(self.identificador)+','+self.nome+','+self.descricao+','+str(self.lance_minimo)+','+str(self.dia)+','+ str(self.mes)+','+str(self.ano)+','+str(self.hora)+','+str(self.minuto)+','+str(self.segundo)+','+str(self.t_max)+','+self.dono+'\n')
"""
Sequência de comandos antiga que salvava no .txt de leilões terminados
        g = open('leilao_finalizados.txt', 'a')  # Escreve as linhas a partir da útlima linha escrita
        g.write(self.nome+','+self.descricao+','+str(self.lance_minimo)+','+str(self.dia)+','+ str(self.mes)+','+str(self.ano)+','+str(self.hora)+','+str(self.minuto)+','+str(self.segundo)+','+str(self.t_max)+','+self.dono+'\n')
"""

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
        f.write(self.nome + ',' + self.telefone + ',' + self.endereco + ',' + self.email + ',' + self.senha+','+self.socket1+','+str(self.indice)+'\n')

class controle_geral: # Classe que controla os usários do sistema de leilão
    lista_usuario = []  # Atributo que lista todos os usuários já cadastrados
    onlines = []  #atributo que guarda os índices na lista_usuario dos usuários que estão online
    lista_leiloes_futuros=[]
    lista_leiloes_correntes=[] # atributo onde estarão os leilões iniciados para monitoramento

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
        print 'Dentro do txt dos usuários tem:\n'
        for i in self.lista_usuario:
            print i.nome+i.socket1

        print '\nDentro do txt dos leilões não terminados tem:\n'
        for i in self.lista_leiloes_futuros:
            print str(i.nome)+', peretecente a '+i.dono+' para dia: '+str(int(i.dia))+'/'+str(int(i.mes))+'/'+str(int(i.ano))+' as '+str(int(i.hora))+','+str(int(i.minuto))+'h\n'

    def __init__(self): #metodo para carregar usuários do txt
        self.onlines = []
        self.lista_usuario=[]
        print 'Inicia controle de usuários\n'
        try:  # Caso o arquivo 'clientes.txt' não exista, ele abre uma exceção de IOError e passa
            f = open('clientes.txt')  # Abre o arquivo clientes
            for linha in f: # Percorre todas as linhas do txt
                linha=linha.split(',')
                usuario = user(str(linha[0]), str(linha[1]), str(linha[2]), str(linha[3]),str(linha[4]),str(linha[5]+','+linha[6]),str(linha[7])) # Transforma linhas do txt em objetos da classe user
                self.lista_usuario.append(usuario)
        except IOError:
            pass
        try: # Caso o arquivo 'clientes.txt' não exista, ele abre uma exceção de IOError e passa
            f = open('leiloes_nao_terminados.txt')  # Abre o arquivo leilões não terminados
            for linha in f:  # Percorre todas as linhas do txt (leilões aqrquivados)
                c = linha.split(',')
                print '1'
                for i in range(3,10):  # Transforma strings de saída do txt em floats
                    c[i]=int(float(c[i]))
                print '2'

                if teste_de_data(c[4], c[5], c[6], c[7], c[8], c[9]) == 1: # Verifica se a data e hora de início de leilões arquivados não expiraramS
                    leilaao = leilao(c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9], c[10], c[11])  # Transforma linhas do txt em objetos da classe user
                    leilaao.identificador=c[0] #Salvando identificador do leilão
                    self.lista_leiloes_futuros.append(leilaao)

                else :
                    #aviso de que algum leilão perdeu a data de inicio com servidor off line
                    print '\nLeião de '+str(c[0])+' teve momento de início perdido com servidor off-line\n'
                print '3'
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
    """
    def checa_senha(self,nome,senha):
        s=0
        for i in self.lista_usuario:
            if i.nome == nome:
                if senha == i.senha:
                    s=1
                    break
        return s
    """
    def add_socket(self,nome, sock): # Função para alterar socket de usuário logado
        for i in self.lista_usuario:
            if i.nome == nome:
                i.socket1=sock

def envio(destinatario,mensagem): # Função para envio de mensagem com repetição em caso de erro na transmisssão
    while(1):
        try:
            destinatario.sendall(mensagem)
            resp=destinatario.recv(1024)
            if resp=='not_ok,err_pct':
                raise
            else:
                break

        except:
            pass

def recebimento(canal):  # Função para recepção de mensagens com repetição em cas de erro da transmissão
    flag=0
    while (1):
        resp=canal.recv(1024)
        try:
            #aqui entra tratamento de erro de pacote, que caso ocorra gera flag=1
            if flag == 1:
                canal.sendall('not_ok,err_pct')
                raise
            else:
                return resp
        except:
            pass

#def envia_listagem():

def teste_de_data(dia,mes,ano,hora,minuto,segundo): # função pra testar se a hora e data do leilão é no futuro

    agora = datetime.datetime.now()  # aquisição de hora e data do pc

    try:
        if ano < float(agora.year):
            print 'ano anterior'
            raise
        elif ano == agora.year:
            if mes < agora.month:
                print 'mês anterior'
                raise
            elif mes == agora.month:
                if dia < agora.day:
                    print 'dia anterior'
                    raise
                elif dia == agora.day:
                    if hora < agora.hour:
                        print 'hora anterior'
                        raise
                    elif hora == agora.hora:
                        if minuto < agora.minute:
                            print 'minuto anterior'
                            raise
                        elif minuto == agora.minute:
                            if segundo < agora.segundo:
                                print 'segundo anterior'
                                raise
                            else:
                                return 1
                        else:
                            return 1
                    else:
                        return 1
                else:
                    return 1
            else:
                return 1
        else:
            return 1


    except:
        # Aviso de que algum leilão foi marcado para antes da data corrente
        print '\nLeilão marcado para antes data atual\n'
        return 0

def listar_leiloes():
    arquivo = 'Listagem\n\n'
    # arquivo = open('leiloes_p_envio.txt',
    #               'w')  # atualizando txt com valor dos leilões ainda não terminados
    cont = 1
    for i in controle.lista_leiloes_futuros:
        arquivo = (arquivo + 'Leilão de ' + str(i.nome) + ',' + str(i.descricao) + ', de lance mínimo de R$ ' + str(
            i.lance_minimo) + '\nMarcado para dia ' + str(i.dia) + '/' + str(i.mes) + '/' + str(i.ano) + ' as ' + str(
            i.hora) + ' horas, ' + str(i.minuto) + ' minutos e ' + str(
            i.segundo) + ' segundos\ncom tempo máximo de ' + str(
            i.t_max) + 'se gundos entre lances e pertencente a ' + str(i.dono) + '\n')
        cont = cont + 1

    conn.sendall(str(arquivo))

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
                    nome = user(a[1],a[2],a[3],a[4],a[5],str(addr),len(controle.lista_usuario)+1) # crio objeto 'nome' da classe usuário
                    name = a[1] # armazenamento do nome do cleinte logado para utilização na criação de leilão
                    #logado.socket=conn
                    print "criei objeto da classe usuário"

                    logado=controle.adc_usuario(nome) #adc usuário ao controle
                    controle.onlines.append(logado)

                    #controle.add_socket(a[1], conn)

                    #logado = controle.retorna_usuario(a[1])
                    print "arquivei usuario"
                    conn.sendall('ok')
                    estado = 1 # # alteração do servidor para switch 2 ao fim do while(1) (logado)
                    break

        elif a[0] == 'Faz_login':
            print 'Faz_login acionado'
            while 1: #Fica no loop para caso a ele erre alguma coisa, tentar novamente
            #Se o nome que ele digitou for igual ao nome e a senha
            # forem iguais as que tenho no regsitro, ele faz o login
            ## print "Entrei login"
            #nome1 = globals()[a[1]].nome #Como fazer a comparação direto?
                try:
                    k1=controle.checar_nome_existente(a[1],1,a[2]) # Verificação se nome existe
                    if (k1 == 1):

                        logado = controle.retorna_usuario(a[1],addr)
                        print 'usuário '+str(logado.nome)+' de índice '+str(logado.indice)+' logado com ip e porta'+str(logado.socket1)
                        name = logado.nome # armazenamento do nome do cleinte logado para utilização na criação de leilão
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
            print 'cliente escolheu listar leilões'
            listar_leiloes()



        elif a[0] == 'Desligar':
                                                             ##
            arquivo = open('leiloes_nao_terminados.txt', 'w') # apagando conteúdo do txt dos leiloes não terminados
            arquivo.close()                                   #
                                                             ##

            arquivo = open('leiloes_nao_terminados.txt', 'w') # atualizando txt com valor dos leilões ainda não terminados
            cont=1
            for i in controle.lista_leiloes_correntes:
                if teste_de_data(i.dia,i.mes,i.ano,i.h,i.minuto,i.segundo)==1:
                    arquivo.write(i.nome + ',' + i.descricao + ',' + str(i.lance_minimo) + ',' + str(i.dia) + ',' + str(i.mes) + ',' + str(i.ano) + ',' + str(i.ano) + ',' + str(i.hora) + ',' + str(i.minuto) + ',' + str(i.segundo) + ',' + str(i.t_max) + ',' + i.dono + +','+str(cont)+'\n')
                    cont=cont+1
                    # aqui vai comando pra matar thread
        while estado == 1: # Switch 2
            print 'switch2\n'
            resp=conn.recv(1024)
            b=resp.split(',')
            if b[0]=='Lanca_produto': # lançamento de novo produto
                print 'trecho de lançamento de produto\n'
                #atrib = [0] * (len(b))  #  lista vazia para armazenamento de

                for i in range(3,10):  # Transforma strings de saída da mensagem em floats
                    b[i] = int(float(b[i]))


                # Verifica se a data e hora de início de leilão não expirarou

                if teste_de_data(b[4], b[5], b[6], b[7], b[8], b[9]) == 1:

                    ##
                    arquivo = open('numero_de_leiloes_cadastrados', 'r')
                    for lin in arquivo:
                        num_leiloes=lin
                        print 'numero de leilões cadastrados aobsorvido '+str(num_leiloes)+'\n'
                    arquivo.close()  #


                    num_leiloes=int(num_leiloes)+1


                    arquivo = open('numero_de_leiloes_cadastrados',
                                   'w')  # apagando conteúdo do txt dos leiloes não terminados
                    arquivo.write(str(num_leiloes))
                    arquivo.close()  #

                    leilaao = leilao( b[1], b[2], b[3], b[4],b[5],b[6],b[7],b[8],b[9],b[10],name)
                    leilaao.identificador=num_leiloes
                    controle.lista_leiloes_correntes.append(leilaao)
                    leilaao.arquivar_leilao()
                    conn.sendall('ok')
                    print 'leilão criado com sucesso\n'
                else:
                    # aviso de que algum leilão perdeu a data de inicio com servidor off line
                    print '\nleilão de ' + str(b[1]) + ' marcado para antes de agora\n'
                    conn.sendall('not_ok')


            elif a[0] == 'Lista_leiloes':

                print 'cliente escolheu listar leilões'

                listar_leiloes()


            else:
                print 'aqui vão entrar as outras opções do switch2'

                estado = 0; #comando provisório para não ter loop infinito






#Tenho que criar um segundo Thread para o leilao


if __name__ == '__main__':  ###Programa principal

    HOST = ''                 # Symbolic name meaning all available interfaces
    PORT = 50000              # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket (TCP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #forçar que o socket desaloque a porta quando fechar o código
    s.bind((HOST, PORT)) #liga o socket com IP e porta

    print "Servidor funcionado"
    print "Esperando pelos clientes\n"
    controle = controle_geral()  # carrega os usuarios que estavam no clientes.txt
    clientes=0
    logado=None
    while 1:
        s.listen(1)
        conn, addr = s.accept()  # Aceita uma conexão
        clientes += 1
        print "Número de clientes conectados", clientes
        t = threading.Thread(target=servidor, args=(conn,addr))
        t.start()
