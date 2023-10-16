from warnin_colors import text_colors
from getpass import getpass
from lista_usuarios_cadastrados import ler_usuarios_cadastrados

def fazer_login(lista_usuarios, lista_adms):
     dados = {
          'nome_usuario': input(text_colors.OKBLUE + 'Digite seu nome: '),
          'senha': getpass(text_colors.OKBLUE + 'Digite sua senha: ')
     }
     
     if(dados['nome_usuario'] == '' or dados['senha']== ''):
          print(text_colors.FAIL + 'Dados inválidos!')
          return 'fail'

     for adm in lista_adms:
          if((adm['nome_usuario'] == dados['nome_usuario']) and (adm['senha'] == dados['senha'])):
               print(text_colors.OKGREEN + 'ADM logado com sucesso!')
               return adm

     for usuario in lista_usuarios:
          if((usuario['nome_usuario'] == dados['nome_usuario']) and (usuario['senha'] == dados['senha'])):
               print(text_colors.OKGREEN + 'USUARIO logado com sucesso!')
               return usuario

     print(text_colors.FAIL + 'Dados inválidos!')

     

     