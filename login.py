from warnin_colors import text_colors

def fazer_login(lista_usuarios, lista_adms):
    dados = []
    nome = input(text_colors.OKBLUE + 'Digite seu nome: ')
    senha = input(text_colors.OKBLUE + 'Digite sua senha: ')

    dados.append(nome)
    dados.append(senha)

    print(lista_usuarios, lista_adms)
    
    for lista in lista_adms:
        if(dados == lista):
            print(text_colors.OKGREEN + 'ADM logado com sucesso!')
            return 'adm logado'
    for lista in lista_usuarios:
        if(dados == lista):
            print(text_colors.OKGREEN + 'USUARIO logado com sucesso!')
            return 'usuario logado'
    
    print(text_colors.FAIL + 'Usuário ou senha inválidos!')



