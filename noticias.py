from warnin_colors import text_colors

noticias = [{
    'id': 1,
    'titulo': 'ET Bilu',
    'autor': 'laires',
    'data': '16/10/2023',
    'texto': 'Se você já acessava a internet em 2010, é bem provável que a frase "busquem conhecimento" te traga lembranças de uma figura bastante inusitada e conhecida entre os brasileiros. O ET Bilu, popularizado no início da década passada, ficou conhecido após ser "entrevistado" por uma emissora nacional e enviar a mensagem para os cidadãos de todo o mundo: busquem conhecimento. A conversa bizarra com ET Bilu — que, inclusive, falava português fluentemente — só foi possível quando o ufólogo Urandir Fernandes, líder da comunidade Projeto Portal, que acolhia o suposto alien, permitiu as gravações. Surpreendentemente, após 12 anos desde a primeira aparição do ET Bilu, Urandir continua dando o que falar no mundo da ufologia. Líder da comunidade Cidade Zigurats (antigo Projeto Portal) até hoje, ele criou a Associação Dakila Pesquisas para "estudar diversas áreas do conhecimento, buscando preencher as lacunas que a literatura tradicional não menciona", segundo o site da instituição. Resumidamente, os moradores de Zigurats estudam civilizações antigas e alienígenas. As crenças da Cidade Zigurats incluem a teoria de que a Terra não é redonda, é convexa. Em 2019, ele foi condecorado com o título de cidadão campo-grandense pela câmara de vereadores da cidade. O reconhecimento, no entanto, foi bastante criticado pela Comissão Brasileira de Ufólogos (CBU), que destacou a falta de credibilidade científica de Urandir. A polêmica mais recente do ufólogo envolve o mito da cidade de Ratanabá. O local, segundo Urandir, fica escondido no meio da Amazônia e abriga seres gigantes. Pesquisadores renomados já desmentiram a suposta civilização escondida.',
    'curtidas': 1450,
    'comentários': {},
    'repostagens': {},
    'compartilhamentos_externos': 0,
    
}]

def visuzlizar_noticia(id): 
    for noticia in noticias:
        if noticia['id'] == int(id):
            print('------------------------------*-----------------------------------')
            print(text_colors.HEADER + noticia['titulo'])
            print(text_colors.OKBLUE + noticia['texto'])
            print('------------------------------*-----------------------------------')
            print(text_colors.BOLD + 'AUTOR: ' + noticia['autor'])
            print(text_colors.BOLD + noticia['data'])
            print(text_colors.BOLD + 'Curtidas: ' + str(noticia['curtidas']))
            print('------------------------------*-----------------------------------')
    pass


def listar_todas_noticias():
    for noticia in noticias :
        print(str(noticia['id']) + ' - ' + noticia['titulo'])

def inserir_noticia_BD(nova_noticia):
    noticias.append(nova_noticia)
    print(nova_noticia)
    pass


def curtir_noticia(noticia_id):
    for noticia in noticias:
        if noticia['id'] == int(noticia_id):
            noticia['curtidas'] += 1
    pass

def comentar_noticia(id):
    pass


def ultimo_id():
    if(len(noticias) == 0): 
        return 0
    return noticias[-1]['id']
