from warnin_colors import text_colors
from getpass import getpass
# Para próxima etapa separar funçao de fazer 
# cadastro da logica de validação de senha

def fazer_cadastro(quem_cadastrar, usuarios_cadastrados, adms_cadastrados):
    while True:
        print(text_colors.OKGREEN + f'Fazendo Cadastro de {quem_cadastrar} ... \n')
        dados_cadastro = [] # no final, nossa funcao devolverá essa lista para o programa principal
        nome_cadastro = input(text_colors.OKBLUE + 'Digite seu nome: ')
        senha_cadastro = getpass(text_colors.OKBLUE + 'Digite sua senha: ')
        confirmacao_senha = getpass(text_colors.OKBLUE + 'Digite novamente sua senha: ')

        # senha e nome não podem ser string vazia
        if((senha_cadastro == confirmacao_senha) and (senha_cadastro != '') and nome_cadastro != ''):
            dados_cadastro.append(nome_cadastro) # aqui usamos append() para inserir os dados do usuário na lista
            dados_cadastro.append(senha_cadastro)
        else: 
            print(text_colors.FAIL + 'Dados inválidos!')
            return

        # Verificamos se o cadastro ja existe
        for usuario in usuarios_cadastrados:
            if(usuario[0] == dados_cadastro[0]):
                print('Usuário já cadastrado')
                return
        for adms in adms_cadastrados:
            if(adms[0] == dados_cadastro[0]):
                print('Usuário já Cadastrado!')
                return

        return dados_cadastro # return devolve para quem o chamou a nossa lista, agora com os dados. E encerra o loop.
  