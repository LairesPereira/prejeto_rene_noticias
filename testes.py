# alunos = { 'rian': 1, 'rene': 3, 'lucas': 10, 'maria': 9, 'Dalina': 2, 'jack': 7}
# alunos_dec = {}

# lista_maiores = []


# while len(alunos) > 0 :
#     maior = 0
#     nome = ''
#     for i in alunos:
#         if alunos[i] > maior:
#             maior = alunos[i]
#             nome = i

#     alunos_dec[nome] = maior
#     lista_maiores.append(nome)
#     del alunos[nome]

# print(lista_maiores)
# print(alunos)
# print(alunos_dec)

# from random import randint
# from PIL import Image
# import psycopg2

# def get_random_profile_pic():
#     img_id = randint(1,5)
#     path = f'static/avatars/Camada_{img_id}.jpg'
#     img = Image.open(path).tobytes()
#     binary = psycopg2.Binary(img)
#     return binary

# get_random_profile_pic()

import re

def validate_login(pswd):

    if len(pswd) > 6:
        for char in pswd:
            if char.isupper():
                return True
        return False
    else:
        return False
    
# validate_login('lairessS')