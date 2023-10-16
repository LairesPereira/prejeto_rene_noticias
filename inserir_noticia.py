from warnin_colors import text_colors
from noticias import ultimo_id, inserir_noticia_BD
from datetime import datetime

def inserir_noticia(usuario):
    escolha = input(text_colors.OKGREEN + 'INSERINDO NOVA NOTÍCIA! Digite enter para continuar ou 0 em qualquer etapa para sair.')
    if escolha == '0': 
        print(text_colors.WARNING + 'Saindo')
        return

    complete = False
    while not complete:
        titulo = input(text_colors.OKBLUE + 'Digite o título da notícia: ')
        texto = input(text_colors.OKBLUE + 'Insira o corpo da notícia: ')
        data = datetime.now()
        data_formatada = str(data.day) + '-' + str(data.month) + '-' + str(data.year) + ' ' + str(data.hour) + ':' + str(data.minute)

        if titulo != '' and texto != '':

            nova_noticia = {
                'id': ultimo_id() + 1,
                'titulo': titulo,
                'autor': usuario['nome_usuario'],
                'data': data_formatada,
                'texto': texto,
                'curtidas': 0,
                'comentários': {},
                'repostagens': {},
                'compartilhamentos_externos': 0,
            }    

            inserir_noticia_BD(nova_noticia)
            complete = True    

        elif titulo == '0' or texto == '0':
            return
        else:
            print(text_colors.FAIL + 'Não deixe campos em branco')
    
 
    

