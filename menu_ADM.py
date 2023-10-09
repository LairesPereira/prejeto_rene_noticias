from warnin_colors import text_colors


def exibir_opcoes_acesso(): 
    print(text_colors.OKCYAN + '1 - Inserir Noticia')
    print(text_colors.OKCYAN + '2 - Listar Noticia')
    print(text_colors.OKCYAN + '3 - Excluir Noticia')
    print(text_colors.OKCYAN + '4 - Editar Noticia')
    print(text_colors.OKCYAN + '5 - Buscar Noticia')
    print(text_colors.OKCYAN + '6 - Sair Noticia')


def menu_ADM():
    exibir_opcoes_acesso()
    opção_menu_adm = input(text_colors.OKGREEN + 'Digite uma opção : ')
    pass






    