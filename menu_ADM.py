from warnin_colors import text_colors
from inserir_noticia import inserir_noticia
# from noticias import listar_todas_noticias, visuzlizar_noticia, remover_noticia_BD, existem_noticias
from noticias import *

def menu_ADM(usuario_logado):
    print(text_colors.OKCYAN + '1 - Inserir Noticia')
    print(text_colors.OKCYAN + '2 - Listar Noticias')
    print(text_colors.OKCYAN + '3 - Excluir Noticia')
    print(text_colors.OKCYAN + '4 - Editar Noticia')
    print(text_colors.OKCYAN + '5 - Buscar Noticia')
    print(text_colors.OKCYAN + '6 - Sair')

    opcao_menu_adm = input(text_colors.OKGREEN + 'Digite uma opção : ')
    if opcao_menu_adm == '1':
        inserir_noticia(usuario_logado)
    
    elif opcao_menu_adm == '2':
        existe_noticia_cadastrada = existem_noticias()
        if existe_noticia_cadastrada:
            listar_todas_noticias()
            opcao_usuario = print(text_colors.BOLD + 'Se desejar ler uma noticia digite o numero correspondente ou 0 para sair')
        else:
            print(text_colors.FAIL + 'Não existem noticias cadastradas!')
            opcao_usuario = '0'

        if opcao_usuario == '0':
            pass
        else:
            noticia_para_ler = input('Digite o numero da notiica que deseja ler: ')
            visuzlizar_noticia(noticia_para_ler)
            interacao = input('Digite 1 para curtir, 2 para comentar ou 0 para sair: ')
            if interacao == '1':
                 curtir_noticia(noticia_para_ler)
            elif interacao == '2':
                 comentario = input('Digite seu comentário: ')
                 comentar_noticia(noticia_para_ler, usuario_logado, comentario)
                 
    
    elif opcao_menu_adm == '3':
            listar_todas_noticias()
            noticia_para_deletar = input('Digite o numero da noticia que deseja deletar: ')
            remover_noticia_BD(noticia_para_deletar)
    
    elif opcao_menu_adm == '4':
            listar_todas_noticias()
            id_alterar = input('Digite a noticia que deseja alterar: ')
            visuzlizar_noticia(id_alterar)
            texto = input('Digite sua alteração: ')
            editar_noticia(id_alterar, texto)
    
    elif opcao_menu_adm == '5':
         listar_noticias_adm(usuario_logado)
    
    elif opcao_menu_adm == '6':
         return
    pass






    