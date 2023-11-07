# AUTORES MONIQUE E LAIRES

from warnin_colors import text_colors
from login import fazer_login
from fazer_cadastro import fazer_cadastro
from lista_usuarios_cadastrados import ler_usuarios_cadastrados, atualizar_usuarios_cadastrados
from menu_ADM import menu_ADM
from menu_usuario  import menu_USUARIO
from art import *

# controle para saber se o usuário está logado
# usuarios e adm cadastros são listas que serão preenchidas
# nas opções de cadastros
# fazer requirementos

login = False

adm_cadastrados = ler_usuarios_cadastrados('ADM')
usuarios_cadastrados = ler_usuarios_cadastrados('USUARIO')
usuario_logado = {}

tprint('breaking news', font='cybermedium') # desenho de boas-vindas
tprint('catolica - pb', font='cybersmall')

# o sistema irá rodar até alguém ou algo interromper o programa
while True:
    if(login): # se houver alguem logado o programa exibe as opcoes de acordo com a categoria isAdm
        if usuario_logado['isAdm']:
            opcao_logado = input(text_colors.OKBLUE + '1 para acessar o menu ADM, 2 para cadastrar ADM, 3 para cadastrar usuário ou 0 para fazer sair: ')
        
        # opcoes de usuario logado
        elif(usuario_logado['isAdm'] == False):
            opcao_logado = input(text_colors.OKBLUE + '1 para acessar o menu, ou 0 para fazer sair: ')
            if(opcao_logado == '1'):
                menu_USUARIO(usuario_logado)
            elif(opcao_logado == '0'):
                break   
        
        if(opcao_logado == '1' and usuario_logado['isAdm'] == True): 
            menu_ADM(usuario_logado)
        elif(opcao_logado == '2' or opcao_logado == '3'):
            cadastrar = 'ADM' if opcao_logado == '2' else 'USUARIO'
            dados_cadastro = fazer_cadastro(cadastrar)
            if(cadastrar == 'ADM' and dados_cadastro): 
                atualizar_usuarios_cadastrados(cadastrar, dados_cadastro)
            elif(cadastrar == 'USUARIO' and dados_cadastro):
                atualizar_usuarios_cadastrados(cadastrar, dados_cadastro)
        elif opcao_logado == '0':
            usuario_logado = {}
            login = False
            pass
        
    else:
        opção_inicial = input(text_colors.OKBLUE + 'Digite 1 para Login, 2 para cadastrar ADM, 3 para cadastrar usuário ou 0 para sair: ')
        
        if(opção_inicial == '1'):
            tentar_logar = fazer_login(usuarios_cadastrados, adm_cadastrados) 
            if(tentar_logar == None):
                continue
            elif(tentar_logar['isAdm']):
                usuario_logado = tentar_logar
                print(text_colors.OKGREEN + 'ADM LOGADO')
                login = True
                menu_ADM(usuario_logado)
            elif(tentar_logar['isAdm'] == False):
                usuario_logado = tentar_logar
                login = True
                menu_USUARIO(usuario_logado)
        # ------------------------------------------------------------------------------------------------------------
        # CADASTRAR
        elif(opção_inicial == '2' or opção_inicial == '3'):
            cadastrar = 'ADM' if opção_inicial == '2' else 'USUARIO'
            dados_cadastro = fazer_cadastro(cadastrar)
            if(cadastrar == 'ADM' and dados_cadastro): 
                atualizar_usuarios_cadastrados(cadastrar, dados_cadastro)
            elif(cadastrar == 'USUARIO' and dados_cadastro):
                atualizar_usuarios_cadastrados(cadastrar, dados_cadastro)
        # ------------------------------------------------------------------------------------------------------------
        elif(opção_inicial == '0'):
            break
        else:
             print(text_colors.FAIL, 'Erro: Entrada inválida')