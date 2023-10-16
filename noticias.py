noticias = [{
    'id': 1,
    'titulo': '',
    'autor': '',
    'data': '',
    'texto': '',
    'curtidas': 0,
    'comentários': {},
    'repostagens': {},
    'compartilhamentos_externos': 0,
}]

def listar_todas_noticias():
    return noticias

def inserir_noticia_BD(nova_noticia):
    noticias.append(nova_noticia)
    print(nova_noticia)
    pass

def ultimo_id():
    if(len(noticias) == 0): 
        return 0
    return noticias[-1]['id']

print(ultimo_id())
