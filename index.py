from warnin_colors import text_colors
from login import fazer_login
from fazer_cadastro import fazer_cadastro
from menu_ADM import menu_ADM
from art import *

# controle para saber se o usuário está logado
# usuarios e adm cadastros são listas que serão preenchidas
# nas opções de cadastros

login = False

# as listas de cadastro tem o formato ['nome', 'senha']
usuarios_cadastrados = []
adm_cadastrados = [['laires', '123']]

tprint('breaking news', font='cybermedium') # desenho de boas-vindas
tprint('catolica - pb', font='cybersmall')

# o sistema irá rodar até alguém ou algo interromper o programa
while login == False:
    if(login):
        # opcoes de usuario logado
        # nesse momento não precisamos dessa opção
        pass 
    else:
        opção_inicial = input(text_colors.OKBLUE + 'Digite 1 para Login, 2 para cadastrar ADM, 3 para cadastrar usuário ou 0 para sair: ')

        # autenticação do usuário (LOGIN)
        # toda a parte de autenticacao fica na resposabilidade de login
        # index vai apenas verificar quem logou e redirecionar para as paginas adqueadas
        if(opção_inicial == '1'):
            tentar_logar = fazer_login(usuarios_cadastrados, adm_cadastrados) 
            if (tentar_logar == 'adm logado'):
                menu_ADM()
            elif(tentar_logar == 'usuario logado'):
                print('CRIAR MENU USUARIO')
        # ------------------------------------------------------------------------------------------------------------
        # CADASTRAR
        elif(opção_inicial == '2' or opção_inicial == '3'):
            cadastrar = 'ADM' if opção_inicial == '2' else 'USUARIO'
            dados_cadastro = fazer_cadastro(cadastrar, usuarios_cadastrados, adm_cadastrados)
            if(cadastrar == 'ADM' and dados_cadastro): 
                adm_cadastrados.append(dados_cadastro)
            elif(cadastrar == 'USUARIO' and dados_cadastro):
                usuarios_cadastrados.append(dados_cadastro)
        # ------------------------------------------------------------------------------------------------------------
        elif(opção_inicial == '0'):
            break
        else:
             print(text_colors.FAIL, 'Erro: Entrada inválida')