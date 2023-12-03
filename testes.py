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
#  
import base64
import random

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Encode the image in base64
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

# Replace 'path/to/your/image.jpg' with the actual path to your JPG image file
image_path = f'static/avatars/avatar_{random.randint(1,5)}.jpg'

# Convert the image to base64
base64_image = image_to_base64(image_path)

# Print or use the base64 representation of the image
print(base64_image)