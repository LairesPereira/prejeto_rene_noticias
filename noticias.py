# -*- coding: UTF-8 -*-

import emoji
from warnin_colors import text_colors

noticias = [{
    'id': 1,
    'titulo': 'ET Bilu',
    'autor': 'laires',
    'data': '16/10/2023',
    'texto': 'Se você já acessava a internet em 2010, é bem provável que a frase "busquem conhecimento" te traga lembranças de uma figura bastante inusitada e conhecida entre os brasileiros. O ET Bilu, popularizado no início da década passada, ficou conhecido após ser "entrevistado" por uma emissora nacional e enviar a mensagem para os cidadãos de todo o mundo: busquem conhecimento. A conversa bizarra com ET Bilu — que, inclusive, falava português fluentemente — só foi possível quando o ufólogo Urandir Fernandes, líder da comunidade Projeto Portal, que acolhia o suposto alien, permitiu as gravações. Surpreendentemente, após 12 anos desde a primeira aparição do ET Bilu, Urandir continua dando o que falar no mundo da ufologia. Líder da comunidade Cidade Zigurats (antigo Projeto Portal) até hoje, ele criou a Associação Dakila Pesquisas para "estudar diversas áreas do conhecimento, buscando preencher as lacunas que a literatura tradicional não menciona", segundo o site da instituição. Resumidamente, os moradores de Zigurats estudam civilizações antigas e alienígenas. As crenças da Cidade Zigurats incluem a teoria de que a Terra não é redonda, é convexa. Em 2019, ele foi condecorado com o título de cidadão campo-grandense pela câmara de vereadores da cidade. O reconhecimento, no entanto, foi bastante criticado pela Comissão Brasileira de Ufólogos (CBU), que destacou a falta de credibilidade científica de Urandir. A polêmica mais recente do ufólogo envolve o mito da cidade de Ratanabá. O local, segundo Urandir, fica escondido no meio da Amazônia e abriga seres gigantes. Pesquisadores renomados já desmentiram a suposta civilização escondida.',
    'curtidas': 1450,
    'comentarios': [{'autor': 'laires', 'comentario': 'comentario 1'}, {'autor': 'felipe', 'comentario': 'comentario 2'}],
    'repostagens': {},
    'compartilhamentos_externos': 0,
    'removida': False
},
{
    'id': 2,
    'titulo': 'Noticia 2',
    'autor': 'felipe',
    'data': '16/10/2023',
    'texto': 'O Rio registrou neste domingo (12) até as 14h uma temperatúra máxima de 40,4ºC. O registro foi feito às 14h, na estação da Vila Militar do Inmet, na Zona Oeste do Rio. Foi a maior temperatura do ano na cidade, segundo o Inmet. Também de acordo com o instituto, com os registros que deram entrada no sistema até 16h30, o Rio é a capital onde fez mais calor neste domingo. De acordo com o Centro de Operações da Prefeitura, fez ainda mais calor: 42,5ºC, na Estação Irajá. A prefeitura também registrou sensação térmica de 50,5°C em Irajá, às13h55. Ela não configurou, porém, recorde do ano, que foi registrado em fevereiro, com 58,3°C.',
    'curtidas': 1450,
    'comentarios': [{'autor': 'laires', 'comentario': 'comentario 1'}, {'autor': 'felipe', 'comentario': 'comentario 2'}],
    'repostagens': {},
    'compartilhamentos_externos': 0,
    'removida': False
}
]

def existem_noticias():
    for noticia in noticias:
        if noticia['removida'] == False:
            return True
    return False

def listar_todas_noticias(): 
    for noticia in noticias :
        if noticia['removida']:
            continue
        print(str(noticia['id']) + ' - ' + noticia['titulo'])
           
def inserir_noticia_BD(nova_noticia):
    noticias.append(nova_noticia)
    pass

def remover_noticia_BD(noticia_id):
    for noticia in noticias:
        if noticia['id'] == int(noticia_id):
            noticia['removida'] = True
            return True
    return False

def curtir_noticia(noticia_id):
    for noticia in noticias:
        if noticia['id'] == int(noticia_id):
            noticia['curtidas'] += 1
    pass

def comentar_noticia(noticia_id, usuario, comentario):
    for noticia in noticias:
        if noticia['id'] == int(noticia_id):
            noticia['comentarios'].append({
                'autor': usuario['nome_usuario'],
                'comentario': comentario
            })
    pass

def ultimo_id():
    if(len(noticias) == 0): 
        return 0
    return noticias[-1]['id']

def exibir_comentarios(index):
    # header dos comentarios
    print('------------------------------*-----------------------------------')
    print(text_colors.HEADER + 'COMENTÁRIOS')
    print('------------------------------*-----------------------------------')
    comentarios = noticias[index]['comentarios']

    for comentario in comentarios:
        print(emoji.emojize(":nerd_face: "), end=' ')
        print(text_colors.BOLD + 'Autor: ' + comentario['autor'])
        print(emoji.emojize(":speech_balloon: "), end=' ')
        print(text_colors.BOLD + comentario['comentario'])
        print('\n')
    pass

def visuzlizar_noticia(id): 
    for noticia in noticias:
        if noticia['removida']: 
            continue
        if noticia['id'] == int(id):
            
            print('------------------------------*-----------------------------------')
            print('\n')
            print(text_colors.HEADER + noticia['titulo'])
            print('\n')
            print(text_colors.OKBLUE + noticia['texto'])
            print('\n')
            print('------------------------------*-----------------------------------')

            print(emoji.emojize(":writing_hand_light_skin_tone: "), end=' ')
            print(text_colors.BOLD + 'AUTOR: ' + noticia['autor'])
            print(emoji.emojize(":calendar:"), end=' ')
            print(text_colors.BOLD + noticia['data'])
            print(emoji.emojize(":red_heart: "), end=' ')
            print(text_colors.BOLD + 'Curtidas: ' + str(noticia['curtidas']))
            print('------------------------------*-----------------------------------')
            
            exibir_comentarios(noticias.index(noticia))

            print('------------------------------*-----------------------------------')
    pass

def buscar_noticia(texto): 
    if len(texto) == 0:
        print('Pesquisa Inválida')
        return

    resultado = []
    texto_dividido = texto.split(' ') # separa a string que o usuario digitou em uma lista de palavras
    matches = []

    if existem_noticias():
        for noticia in noticias:
            for palavra in texto_dividido:
                if palavra in noticia['texto']:
                    matches.append(noticia['id'])

        if len(matches):
            for match in matches:
                visuzlizar_noticia(match)
        else:
            print('Nenhuma Notícia encontrada')
    else:
        print('Não há notícias cadastradas. ')

def editar_noticia(id, novo_texto):
    if len(novo_texto) == 0 :
        print('Alteração inválida!')

    for noticia in noticias:
        if noticia['id'] == int(id):
            noticia['texto'] = novo_texto

def listar_noticias_adm(usuario):
    print(usuario)
    listagem = []
    for noticia in noticias:
        if noticia['autor'] == usuario['nome_usuario']:
            listagem.append(noticia['id'])
    
    for id in listagem:
        visuzlizar_noticia(id)