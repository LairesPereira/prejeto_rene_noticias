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

# import re

# def validate_login(pswd):

#     if len(pswd) > 6:
#         for char in pswd:
#             if char.isupper():
#                 return True
#         return False
#     else:
#         return False
    
# validate_login('lairessS')

# from email_validator import validate_email, EmailNotValidError

# email = "laires@gmail"

# try:

#   # Check that the email address is valid. Turn on check_deliverability
#   # for first-time validations like on account creation pages (but not
#   # login pages).
#   emailinfo = validate_email(email, check_deliverability=False)
#   print('aqui')
#   # After this point, use only the normalized form of the email address,
#   # especially before going to a database query.
#   email = emailinfo.normalized
# except EmailNotValidError as e:

#   # The exception message is human-readable explanation of why it's
#   # not a valid (or deliverable) email address.
# #  
# import base64
# import random

# def image_to_base64(image_path):
#     with open(image_path, "rb") as image_file:
#         # Encode the image in base64
#         encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
#     return encoded_image

# # Replace 'path/to/your/image.jpg' with the actual path to your JPG image file
# image_path = f'static/avatars/avatar_{random.randint(1,5)}.jpg'

# # Convert the image to base64
# base64_image = image_to_base64(image_path)

# # Print or use the base64 representation of the image
# print(base64_image)

# from datetime import datetime

# def get_date():
#     now = datetime.now()
#     date = now.strftime("%d/%m/%Y")
#     print(date)

# get_date()

# from PIL import Image
# import os

# image = Image.open('static/avatars/IMG_9684.JPG')

# width, height = image.size
# new_size = (width//2, height//2)
# resized_image = image.resize(new_size)

# resized_image.save('compressed_image.jpg', optimize=True, quality=50)

# original_size = os.path.getsize('image.jpg')
# compressed_size = os.path.getsize('compressed_image.jpg')

# print("Original Size: ", original_size)
# print("Compressed Size: ", compressed_size)

import subprocess
import time
from dao import *

while True:
    conexao = conectardb()
    cur = conexao.cursor()
    while True:
        try:
            cur.execute('SELECT * FROM pg_stat_activity')
        except psycopg2.IntegrityError:
            conexao.rollback()
            break
        else:
            results = cur.fetchall()
            for result in results:
                print('datname: ', result[1])
                print('username: ', result[5])
                print('appname: ', result[6])
                print('clientaddr: ', result[7])
                print('state: ', result[16])
                print('*' * 100)
            time.sleep(1)  # intervalo de 5 segundos 

    conexao.close()
    cur.close()