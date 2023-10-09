from warnin_colors import text_colors

def fazer_login():
    dados_do_usuario = []
    nome_de_usuario = input(text_colors.OKBLUE + 'Digite seu nome: ')
    senha_do_usuario = input(text_colors.OKBLUE + 'Digite sua senha: ')
    
    dados_do_usuario.append(nome_de_usuario)
    dados_do_usuario.append(senha_do_usuario)

    return dados_do_usuario



