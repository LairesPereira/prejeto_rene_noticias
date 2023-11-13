from warnin_colors import text_colors
from inserir_noticia import inserir_noticia
from noticias import *

def menu_USUARIO(usuario_logado):
    #  exibir opções que o usuario pode realizar
    print(text_colors.OKCYAN + '1 - Listar Noticia')
    print(text_colors.OKCYAN + '2 - Ler Noticias')
    print(text_colors.OKCYAN + '3 - Buscar Noticia')
    print(text_colors.OKCYAN + '4 - Comentar Noticia')

    opcao_menu_usuario = input(text_colors.OKGREEN + 'Digite uma opção : ')
    if opcao_menu_usuario == '1':
            listar_todas_noticias()
    elif opcao_menu_usuario == '2':
            listar_todas_noticias()
            noticia_escolhida = input('Digite o numero da notiica que deseja ler ou 0 para sair: ')
            if noticia_escolhida == '0':
                pass
            else:
                visuzlizar_noticia(noticia_escolhida)
                acao_noticia = input('Digite 1 para curtir a notícia ou 2 para comentar a noticia: ')
                if acao_noticia == '1':
                    curtir_noticia(noticia_escolhida)
                elif acao_noticia == '2':
                     comentario = input('Digite seu comentario: ')
                     if comentario == '':
                          pass
                     comentar_noticia(noticia_escolhida, usuario_logado, comentario)
    elif opcao_menu_usuario == '3':
        pesquisa_usuario = input('Digite o que deseja buscar: ')
        buscar_noticia(pesquisa_usuario)

         
                # curtir_noticia = input('Digite o numero da notiica que deseja ler ou 0 para sair: ')
                # comentar_noticia = input('Digite o numero da notiica que deseja ler ou 0 para sair: ')
