from warnin_colors import bcolors

def fazer_cadastro(quem_cadastrar):
    while True:
        print(bcolors.OKGREEN + f'Fazendo Cadastro de {quem_cadastrar} ... \n')
        
        dados_cadastro = [] # no final, nossa funcao devolverá essa lista para o programa principal
        nome_cadastro = input(bcolors.OKBLUE + 'Digite seu nome: ')
        senha_cadastro = input(bcolors.OKBLUE + 'Digite sua senha: ')
        confirmacao_senha = input(bcolors.OKBLUE + 'Digite novamente sua senha: ')

        if(senha_cadastro == confirmacao_senha):
            dados_cadastro.append(nome_cadastro) # aqui usamos append() para inserir os dados do usuário na lista
            dados_cadastro.append(senha_cadastro)
            return dados_cadastro # return devolve para quem o chamou a nossa lista, agora com os dados. E encerra o loop.
        else: 
            print(bcolors.FAIL + 'Você digitou a senha errada!')
