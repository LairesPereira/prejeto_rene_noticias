from warnin_colors import text_colors
from getpass import getpass
from lista_usuarios_cadastrados import ler_usuarios_cadastrados, atualizar_usuarios_cadastrados
# Para próxima etapa separar funçao de fazer 
# cadastro da logica de validação de senha

usuarios_cadastrados = ler_usuarios_cadastrados('USUARIOS')
adms_cadastrados = ler_usuarios_cadastrados('ADM')

def fazer_cadastro(quem_cadastrar):
    while True:
        print(text_colors.OKGREEN + f'Fazendo Cadastro de {quem_cadastrar} ... \n')
        nome_usuario = input(text_colors.OKBLUE + 'Digite seu nome de usuário: ')
        nome_completo = input(text_colors.OKBLUE + 'Digite seu nome completo: ')
        senha = getpass(text_colors.OKBLUE + 'Digite sua senha: ')
        confirmacao_senha = getpass(text_colors.OKBLUE + 'Digite sua senha novamente: ')

        dados_cadastro = { # no final, nossa funcao devolverá essa lista para o programa principal
            'nome_usuario': nome_usuario,
            'senha': senha,
            'nome_completo': nome_completo,
            'cpf': '433.941.708.41',
            'noticias_publicadas': {},
            'noticias_favoritas': {},
            'noticias_compartilhaads': {},
            'comentarios_em_noticias': {},
        }


        # senha e nome não podem ser string vazia
        if((dados_cadastro['senha'] == confirmacao_senha) and (dados_cadastro['senha'] != '') and dados_cadastro['nome_usuario'] != ''):
            print(usuarios_cadastrados)
            for usuario in usuarios_cadastrados:
                if(usuario['nome_usuario'] == dados_cadastro['nome_usuario']):
                    print('Usuário já cadastrado')
                    return
            for adms in adms_cadastrados:
                if(adms['nome_usuario'] == dados_cadastro['nome_usuario']):
                    print('Usuário já Cadastrado!')
                    return

        else: 
            print(text_colors.FAIL + 'Dados inválidos!')
            return
        

        # Verificamos se o cadastro ja existe
        return dados_cadastro # return devolve para quem o chamou a nossa lista, agora com os dados. E encerra o loop.
  