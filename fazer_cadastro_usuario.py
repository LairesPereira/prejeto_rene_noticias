from warnin_colors import bcolors

def fazer_cadastro_usuario():
    while True:
        print(bcolors.OKGREEN + 'Fazendo Cadastro de usuário... \n')
        
        dados_usuario_cadastro = [] # no final, nossa funcao devolverá essa lista para o programa principal
        nome_usuario_cadastro = input(bcolors.OKBLUE + 'Digite seu nome: ')
        senha_usuario_cadastro = input(bcolors.OKBLUE + 'Digite sua senha: ')
        confirmacao_senha = input(bcolors.OKBLUE + 'Digite novamente sua senha: ')

        if(senha_usuario_cadastro == confirmacao_senha):
            dados_usuario_cadastro.append(nome_usuario_cadastro) # aqui usamos append() para inserir os dados do usuário na lista
            dados_usuario_cadastro.append(senha_usuario_cadastro)
            return dados_usuario_cadastro # return devolve para quem o chamou a nossa lista, agora com os dados. E encerra o loop.
        else: 
            print(bcolors.FAIL + 'Você digitou a senha errada!')
