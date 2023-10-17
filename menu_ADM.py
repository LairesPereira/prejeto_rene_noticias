from warnin_colors import text_colors
from inserir_noticia import inserir_noticia
from noticias import listar_todas_noticias, visuzlizar_noticia

def menu_ADM(usuario_logado):
    print(text_colors.OKCYAN + '1 - Inserir Noticia')
    print(text_colors.OKCYAN + '2 - Listar Noticias')
    print(text_colors.OKCYAN + '3 - Excluir Noticia')
    print(text_colors.OKCYAN + '4 - Editar Noticia')
    print(text_colors.OKCYAN + '5 - Buscar Noticia')
    print(text_colors.OKCYAN + '6 - Sair Noticia')

    opcao_menu_adm = input(text_colors.OKGREEN + 'Digite uma opção : ')
    if opcao_menu_adm == '1':
        inserir_noticia(usuario_logado)
    elif opcao_menu_adm == '2':
        listar_todas_noticias()
        opcao_usuario = print(text_colors.BOLD + 'Se desejar ler uma noticia digite o numero correspondente ou 0 para sair')
        if opcao_usuario == '0':
            pass
        else:
            noticia_para_ler = input('Digite o numero da notiica que deseja ler: ')
            visuzlizar_noticia(noticia_para_ler)
            
                 
    pass






    