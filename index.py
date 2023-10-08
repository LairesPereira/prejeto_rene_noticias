from warnin_colors import bcolors
from login import fazer_login
from fazer_cadastro_adm import fazer_cadastro_adm
from fazer_cadastro_usuario import fazer_cadastro_usuario

# controle para saber se o usuário está logado
# usuarios e adm cadastros são listas que serão preenchidas
# nas opções de cadastros

login = False
usuarios_cadastrados = []
adm_cadastrado = []

# o sistema irá rodar até alguém ou algo interromper o programa
while login == False:
    if(login):
        # opcoes de usuario logado
        # nesse momento não precisamos dessa opção
        pass # pass siginifica pular esse trecho
    else:
        # perguntamos o que o usuário quer fazer
        opção_inicial = int(input(bcolors.OKBLUE + 'Digite 1 para Login, 2 para cadastrar ADM, 3 para cadastrar usuário ou 0 para sair '))
        
        # autenticação do usuário (LOGIN)
        if(opção_inicial == 1):
            # chamamos uma função de login para resolver as informações do usuário
            # a função fazer login nos retorna uma lista contendo ['nome', 'senha'] nas posições 0 e 1
            dados_do_usuario = fazer_login() 

            # usamos len() para saber o tamanho da lista de usuarios cadastrados, se for 
            # se o tamanho for 0 a lista está vazia e não temos como fazer o login
            # se for maior que zero, existe alguem na lista e verificamos se os dados digitados na funcao
            # fazer login batem com os dados do usuario cadastrado.
            if((len(usuarios_cadastrados) > 0 ) and (dados_do_usuario[0] == usuarios_cadastrados[0])):
                # se o usuário estiver cadastrado verificamos a senha que está na posição 1 da lista
                if(dados_do_usuario[1] == usuarios_cadastrados[1]):
                    print(bcolors.OKGREEN + 'Você foi logado com sucesso!')

                    # se a senha estiver correta nós mudamos a variável login para True
                    # encerrando o nosso loop para encaminharmos o usuário para outra tela (futuramente no projeto)
                    login = True
                    # CRIAR MENU DE USUARIO LOGADO

                else:
                    # se qualquer uma das verificações falharem nós repetimos o loop
                    print(bcolors.FAIL + 'Usuário ou senha inválidos!')
            else:
                print(bcolors.FAIL + 'Usuário ou senha inválidos!')

        # ------------------------------------------------------------------------------------------------------------
        
        # CADASTRAR ADM
        elif(opção_inicial == 2):
             # chaamos uma função especifica da mesma forma da anterior, 
             # LEMBRE QUE ELA RETORNA UMA LISTA contendo as informacoes fornecidas pelo adm
            dados_adm_cadastro = fazer_cadastro_adm()

            # aqui, entretando não podemos colocar a resposta da função fazer cadastro
            # diretamente dentro da lista pois estariamos inserindo uma lista dentro de outra
            nome_adm = dados_adm_cadastro[0] # "desmontamos" a lista dentro de outras variáveis
            senha_adm = dados_adm_cadastro[1]
            adm_cadastrado.append(nome_adm) # e só então colocamos cada peça dentro da lista de cadastrados
            adm_cadastrado.append(senha_adm)
            print(bcolors.OKGREEN + 'ADM cadastrado com sucesso!')
            #
            # Leva-lo para página de ADM
            #
        
        # ------------------------------------------------------------------------------------------------------------

        elif(opção_inicial == 3):
            dados_usuario_cadastro = fazer_cadastro_usuario()
            nome_usuario = dados_usuario_cadastro[0]
            senha_usuario = dados_usuario_cadastro[1]
            usuarios_cadastrados.append(nome_usuario)
            usuarios_cadastrados.append(senha_usuario)
            print(bcolors.OKGREEN + 'Usuário cadastrado com sucesso!')
            #
            # Leva-lo para página de usuário
            #
        
        elif(opção_inicial == 0):
            break