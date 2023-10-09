from warnin_colors import text_colors
from getpass import getpass

def fazer_login(lista_usuarios, lista_adms):
        dados = []
        nome = input(text_colors.OKBLUE + 'Digite seu nome: ')
        senha = getpass(text_colors.OKBLUE + 'Digite sua senha: ')
        dados.append(nome)
        dados.append(senha)

        # fazer login recebe do programa principal as duas listas
        # de usuarios e adms cadastras e faz um loop sobre cada uma
        # se a lista de dados que o usuario inseriu para login for igual
        # a alguma das listas recebidas liberamos o login de volta para o programa principal
        for lista in lista_adms:
            if(dados == lista):
                print(text_colors.OKGREEN + 'ADM logado com sucesso!')
                return 'adm logado'
        for lista in lista_usuarios:
            if(dados == lista):
                print(text_colors.OKGREEN + 'USUARIO logado com sucesso!')
                return 'usuario logado'
        
        print(text_colors.FAIL + 'Usuário ou senha inválidos!')
