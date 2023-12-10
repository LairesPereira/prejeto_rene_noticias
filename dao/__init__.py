from datetime import datetime
import psycopg2
from decouple import config
import random
import base64

def conectardb():
    print('Conecatando')
    con = psycopg2.connect(
        host=config("HOST_DATABASE"),
        database=config("DATABASE_NAME"),
        user=config("DATABASE_USER"),
        password=config("DATABASE_PASS")
    )

    return con

def close_conection(conexao):
    print('Fechando conexao')
    if conexao:
        conexao.close()
        return
    return

def get_news_ID(title, conexao=None):
    print('get news id')
    if not conexao:
        conexao = conectardb()

    cur = conexao.cursor()

    query = f"SELECT id FROM noticia WHERE titulo = '{title}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        id = cur.fetchall()
        return id[0][0]

def articles_user_like(user, conexao=None):
    print('articles user like')
    if not conexao:
        conexao = conectardb()

    cur = conexao.cursor()

    query = f"SELECT noticia FROM curtida WHERE usuario = '{user}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        likes = cur.fetchall()
        return likes


def random_profile_pic():
    image_path = f'static/avatars/avatar_{random.randint(1,5)}.jpg'
    with open(image_path, "rb") as image_file:
        # Encode the image in base64
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_image

def get_user_info(user):
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT * FROM usuario WHERE nome_usuario = '{user}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        result = cur.fetchall()
    
    conexao.close()
    cur.close()
    return result

def get_last_id(column):
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT MAX(id) FROM {column};"
    
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
        conexao.close()
        cur.close()
        return
    else:
        fetch = cur.fetchall()
        if fetch[0][0] == None:
            return 1
        return fetch[0][0]
    

def get_news_id_by_title(title, conexao=None):
    print('get news id by title')
    if not conexao:
        conexao = conectardb()

    cur = conexao.cursor()

    query = f"SELECT id FROM noticia where titulo = '{title}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        id = cur.fetchall()
    
    return id[0][0]

def get_users(login, pswd, conexao=None): 
    print('get users')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT * FROM usuario WHERE nome_usuario = '{login}' AND senha = '{pswd}'"
    
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        user = cur.fetchall()
         
    return user

def create_user_db(name, password, email, isadm, conexao=None):
    print('create user db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()
    
    query_check_email_exists= f"SELECT * FROM usuario WHERE nome_usuario = '{name}' OR email = '{email}';"

    user_already_exists = False
    user = []
    insert_result = False

    try:
        cur.execute(query_check_email_exists)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        fetch = cur.fetchall()
        if len(fetch): 
            user_already_exists = True
            user = fetch

    if not user_already_exists:        

        sql = "INSERT INTO usuario (nome_usuario, senha, email, isadm, id, profile_pic) VALUES (%s, %s, %s, %s, %s, %s);"
        last_id = get_last_id('usuario')
        try:
            cur.execute(sql, (name, password, email, isadm, last_id + 1, random_profile_pic()))
        except psycopg2.IntegrityError:
            conexao.rollback()
        else:
            conexao.commit()
            insert_result = True

        return [user_already_exists, insert_result, user]
    return [user_already_exists, insert_result, user]

def check_news_title_exists(title, conexao=None):
    print('check news title exists')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT * FROM noticia WHERE titulo = '{title}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        result = cur.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
    return 

def create_article_db(noticias, conexao=None):
    print('create article db') 
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    titulo, autor, curtidas, removida, corpo, comentarios = noticias
    # "INSERT INTO minha_tabela (meu_campo_texto) VALUES (?)", (minha_string,)
    sql = "INSERT INTO noticia (titulo, autor, curtidas, removida, corpo, comentarios, data_criacao) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    try:
        cur.execute(sql, (titulo.strip(), autor, curtidas, removida, corpo, comentarios, date))
        sucess = True
    except psycopg2.IntegrityError:
        conexao.rollback()
        sucess = False
    else:
        conexao.commit()
    return sucess

def get_user_articles(user, conexao=None):
    print('get user articles')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    sql = f"SELECT * FROM noticia WHERE autor = '{user}' AND removida = false"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        user_articles = cur.fetchall()
        return user_articles
    return

def get_articles_db(conexao=None):
    print('get articles db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()
    
    sql = "SELECT * FROM noticia WHERE removida = false"
    sql = "SELECT * FROM noticia WHERE removida = false ORDER BY curtidas DESC"
    try: 
        cur.execute(sql)
    except psycopg2.IntegrityError:
        cur.rollback()        
    else:
        articles = cur.fetchall()
    return articles

def get_article(title, user, conexao=None):
    print('get article')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    sql = f"SELECT * FROM noticia WHERE titulo = '{title}' and autor = '{user}'"

    article =[]
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        article = cur.fetchall()
        return article
    return 

def read_article_db(title, conexao=None):
    print('read article db')
    if not conexao:
        conexao = conectardb()
    
    cur = conexao.cursor()

    sql = f"SELECT * FROM noticia WHERE titulo ilike '%{title}%'"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        article = cur.fetchall()
        return article
    
    return article

def delete_article_db(title, usuario, conexao):
    print('delete article db')    
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    sql = f"UPDATE noticia SET removida = True WHERE titulo = '{title}' AND autor = '{usuario}'"
    
    sucess = False
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        sucess = True
        conexao.commit()
    return sucess

def check_like_exists(title, user, news_id, conexao=None):
    print('check like exists')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query_check_like_exist = f"SELECT * FROM curtida WHERE usuario = '{user}' AND noticia = {news_id};"

    try:
        cur.execute(query_check_like_exist)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        like_exists = cur.fetchall()
        return like_exists

def get_total_like(news_id, conexao=None):
    print('get total like')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query_count = f"SELECT COUNT (noticia) FROM curtida WHERE noticia = {news_id}"
    try:
        cur.execute(query_count)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        result = cur.fetchall()
        cur.close()
        return result[0][0]
    cur.close()
    return

def update_total_like(title, news_id, conexao=None):
    print('update total like')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    total_likes = get_total_like(news_id, conexao)

    query = f"UPDATE noticia SET curtidas = {total_likes} WHERE titulo = '{title}'" 
    
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        return
    return


def like_count_DB(title, like_action, user, conexao=None):
    print('like count db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    news_id = get_news_ID(title, conexao)
    like_exists = check_like_exists(title, user, news_id, conexao)

    sql_inc = f"INSERT INTO curtida (usuario, noticia) VALUES ('{user}', {news_id})"
    sql_dec = f"DELETE FROM curtida WHERE usuario = '{user}' AND noticia = {news_id};"
    
    try:
        if len(like_exists) == 0:
            cur.execute(sql_inc)
        else:
            cur.execute(sql_dec)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        update_total_like(title, news_id, conexao)
        return True
    return False

def search_DB(search_news):
    print('search db')
    conexao = conectardb()
    cur = conexao.cursor()

    match = list()
    seacrh_split = search_news.split(' ')
    for word in seacrh_split:
        try:
            query = f"SELECT * FROM noticia WHERE titulo ilike '%{word}%' or corpo ilike '%{word}%'"
            cur.execute(query)
        except psycopg2.IntegrityError:
            conexao.rollback()
        else:
            news = cur.fetchall()
            match.append(news[0])
        

    conexao.close()
    return match

def get_profile_pic_DB(user_name, string:None, conexao=None):
    if not conexao:
        conexao = conectardb()

    print('get profile pic')
    cur = conexao.cursor()
    
    if string == None:
        query = f"SELECT profile_pic FROM usuario WHERE nome_usuario in {user_name}"
    else:
        query = f"SELECT profile_pic FROM usuario WHERE nome_usuario = '{user_name}'"
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        bin_pic = cur.fetchall()
        return bin_pic
    return

def send_update_DB(usuario, old_title, news_title, content, conexao=None):
    print('send update db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    sql = f"UPDATE noticia SET titulo = '{news_title}', corpo = '{content}' WHERE autor = '{usuario}' and titulo = '{old_title}'"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        return True
    return False

def get_last_comment_id():
    print('get las comment id')
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT MAX(id) FROM comentario;"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        last_id = cur.fetchall()
        if not last_id[0][0]:
            last_id = 1
        cur.close()
        conexao.close()
    return last_id

def update_total_comment(title, conexao=None):
    print('update total comment')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query = f"UPDATE noticia SET comentarios = comentarios + 1 WHERE titulo = '{title}'"
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        return
    return

def submit_comment_DB(title, comment, user, conexao=None):
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    id = get_news_id_by_title(title, conexao)
    # last_comment_id = get_last_comment_id()

    sql = f"INSERT INTO comentario (id, comentario, autor) VALUES ({id}, '{comment}', '{user}')"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()

def get_news_comments(title, conexao=None):
    print('get news comments')
    if not conexao:
        conexao = conectardb()

    cur = conexao.cursor()

    id = get_news_id_by_title(title, conexao)

    query = f"SELECT * FROM comentario WHERE id = {id}"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        comments = cur.fetchall()
    return comments

def upload_profile_pic_DB(user, image_base64):
    print('upload profile pic')
    conexao = conectardb()
    cur = conexao.cursor()

    try:
        cur.execute(f"UPDATE usuario SET profile_pic = %s WHERE nome_usuario = %s", (image_base64, user))
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()


def search_articles_DB(search, conexao=None):
    print('search articles db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT * FROM noticia WHERE titulo ilike '%{search}%' or corpo ilike '%{search}%'"
    
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else: 
        fetch = cur.fetchall()
        return fetch


def update_profile_BD(user, full_name, city, phone, birthday, conexao=None):
    print('update profile db')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    query = f"UPDATE usuario SET nome_completo = '{full_name}', cidade = '{city}', telefone = '{phone}', nascimento = '{birthday}' WHERE nome_usuario = '{user}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
    return

def get_news_likes(title, conexao=None):
    print('get news likes')
    if not conexao:
        conexao = conectardb()
    cur = conexao.cursor()

    news_id = get_news_ID(title, conexao)
    query = f"SELECT usuario FROM curtida WHERE noticia = {news_id}"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        likes = cur.fetchall()
        return likes
    return
