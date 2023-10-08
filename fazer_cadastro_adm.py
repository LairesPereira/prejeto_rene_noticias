from warnin_colors import bcolors

def fazer_cadastro_adm():
    while True:
        print(bcolors.OKGREEN + 'Fazendo Cadastro de ADM... \n')
        
        dados_adm_cadastro = []
        nome_adm_cadastro = input(bcolors.OKBLUE + 'Digite seu nome: ')
        senha_adm_cadastro = input(bcolors.OKBLUE + 'Digite sua senha: ')
        confirmacao_senha = input(bcolors.OKBLUE + 'Digite novamente sua senha: ')

        if(senha_adm_cadastro == confirmacao_senha):
            dados_adm_cadastro.append(nome_adm_cadastro)
            dados_adm_cadastro.append(senha_adm_cadastro)
            return dados_adm_cadastro
        else: 
            print(bcolors.FAIL + 'Você digitou a senha errada!')




