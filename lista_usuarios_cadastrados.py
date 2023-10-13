# as listas de cadastro tem o formato [['nome', 'senha']]
usuarios_cadastrados = [{
    'id': '1', 
    'nome_usuario': 'monique',
    'senha': '123',
    'nome_completo': 'laires pereira soares',
    'cpf': '433.941.708.41',
    'noticias_publicadas': {},
    'noticias_favoritas': {},
    'noticias_compartilhaads': {},
    'comentarios_em_noticias': {},
},
]


adm_cadastrados = [{
    'id': '1', 
    'nome_usuario': 'laires',
    'senha': '123',
    'nome_completo': 'laires pereira soares',
    'cpf': '433.941.708.41',
    'noticias_publicadas': {},
    'noticias_favoritas': {},
    'noticias_compartilhaads': {},
    'comentarios_em_noticias': {},
},
{
    'id': '2', 
    'nome_usuario': 'rene',
    'senha': '123',
    'nome_completo': 'laires pereira soares',
    'cpf': '433.941.708.41',
    'noticias_publicadas': {},
    'noticias_favoritas': {},
    'noticias_compartilhaads': {},
    'comentarios_em_noticias': {},
}
]


def ler_usuarios_cadastrados(tipo_usuario):
    if tipo_usuario == 'ADM':
        return adm_cadastrados
    else:
        return usuarios_cadastrados

def atualizar_usuarios_cadastrados(tipo_usuario, novo_usuario):
    if tipo_usuario == 'ADM':
        adm_cadastrados.append(novo_usuario)
    else:
        usuarios_cadastrados.append(novo_usuario)