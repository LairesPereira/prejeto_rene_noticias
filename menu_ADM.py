from warnin_colors import text_colors
from inserir_noticia import inserir_noticia

def menu_ADM():
    print(text_colors.OKCYAN + '1 - Inserir Noticia')
    print(text_colors.OKCYAN + '2 - Listar Noticia')
    print(text_colors.OKCYAN + '3 - Excluir Noticia')
    print(text_colors.OKCYAN + '4 - Editar Noticia')
    print(text_colors.OKCYAN + '5 - Buscar Noticia')
    print(text_colors.OKCYAN + '6 - Sair Noticia')

    opcao_menu_adm = input(text_colors.OKGREEN + 'Digite uma opção : ')
    if opcao_menu_adm == '1':
        inserir_noticia()
    pass






    