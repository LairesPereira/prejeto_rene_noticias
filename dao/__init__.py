import psycopg2
# from datetime import datetime
from decouple import config
import random
# from index import get_random_profile_pic

def conectardb():
    con = psycopg2.connect(
        host=config("HOST_DATABASE"),
        database=config("DATABASE_NAME"),
        user=config("DATABASE_USER"),
        password=config("DATABASE_PASS")
    )

    return con

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

def get_news_id_by_title(title):
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT id FROM noticia where titulo = '{title}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        id = cur.fetchall()
    
    cur.close()    
    conexao.close()
    return id[0][0]

def get_users(login, pswd): 
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT * FROM usuario WHERE nome_usuario = '{login}' AND senha = '{pswd}'"
    
    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        user = cur.fetchall()
        conexao.close()
        
    return user

def create_user_db(name, password, email, conexao, isadm):
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

        sql = f"insert into usuario values ('{name}', '{password}', null, null, '{isadm}', '{email}', null)"
        
        try:
            cur.execute(sql)
        except psycopg2.IntegrityError:
            conexao.rollback()
        else:
            conexao.commit()
            insert_result = True

        conexao.close()
        return [user_already_exists, insert_result, user]
    
    return [user_already_exists, insert_result, user]

def create_article_db(noticias, conexao):
    cur = conexao.cursor()

    titulo, autor, curtidas, removida, corpo = noticias

    # sql = "INSERT INTO usuario VALUES ('Rene', '123', 'Rene Gadelha', '123456', True, 'lairespsoares@gmai.com')"

    sql = f"INSERT INTO noticia (titulo, autor, curtidas, removida, corpo) VALUES ('{titulo.strip()}', '{autor}', '{curtidas}', '{removida}', '{corpo}')"
    try:
        cur.execute(sql, (titulo, autor, curtidas, removida, corpo))
        sucess = True

    except psycopg2.IntegrityError:
        conexao.rollback()
        sucess = False

    else:
        conexao.commit()
    return sucess

def get_user_articles(user):
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
    
    conexao.close()
    return

def get_articles_db(): 
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
        conexao.close()
    return articles

def get_article(title, user):
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
        conexao.close()
        return article

    conexao.close()
    return 

def read_article_db(title):
    conexao = conectardb()
    cur = conexao.cursor()

    sql = f"SELECT * FROM noticia WHERE titulo = '{title}' "

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        article = cur.fetchall()
        conexao.close()
        return article
    
    conexao.close()
    return article

def delete_article_db(title, usuario):
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

    conexao.close()
    return sucess

def like_count_DB(title, like_action):
    conexao = conectardb()
    cur = conexao.cursor()

    sql_inc = f"UPDATE noticia SET curtidas = curtidas + 1 WHERE titulo = '{title}'"
    sql_dec = f"UPDATE noticia SET curtidas = curtidas - 1 WHERE titulo = '{title}'"

    try:
        if like_action == 'true':
            cur.execute(sql_inc)
        else:
            cur.execute(sql_dec)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        conexao.close()
        return True
    return False

def search_DB(search_news):
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

def get_profile_pic_DB(user_name):
    conexao = conectardb()
    cur = conexao.cursor()

    query = f"SELECT profile_pic FROM usuario WHERE nome_usuario = '{user_name}'"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        bin_pic = cur.fetchall()
        conexao.close()
        cur.close()
        return bin_pic
    return


noticias = [
    'Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.',
    
    'Professores visionários da Universidade Y foram reconhecidos internacionalmente por sua pesquisa inovadora. Suas contribuições estão moldando o futuro das ciências e inspirando uma nova geração de acadêmicos. Ut efficitur libero nec nisi facilisis, vel tincidunt tellus ultrices. Maecenas in metus ac mauris gravida bibendum. In vestibulum malesuada nunc, vel sollicitudin metus malesuada a. Curabitur sed quam sit amet dolor hendrerit posuere nec ut quam.',

    'Alunos dedicados da Faculdade Z uniram forças para organizar um evento de voluntariado na comunidade local. A iniciativa visa criar impacto positivo e fortalecer os laços entre a academia e a sociedade. Vestibulum rhoncus auctor metus, id sagittis nisi ullamcorper non. Donec sit amet facilisis tellus. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.',

    'A Universidade W está comprometida com a excelência acadêmica e lançou um programa abrangente de bolsas de estudo para apoiar estudantes talentosos. Esta iniciativa visa tornar a educação superior acessível a todos. Nulla facilisi. Fusce tincidunt metus vel est cursus, at malesuada justo finibus. Aenean in sapien quam. Integer congue, augue ut bibendum dapibus, sapien velit interdum purus, in imperdiet libero ex sit amet leo. Duis bibendum, libero in ultricies imperdiet.',

    'A equipe de robótica da Universidade P alcançou um marco significativo ao desenvolver um protótipo avançado para exploração espacial. Suas conquistas estão pavimentando o caminho para futuras missões interplanetárias. Nullam in venenatis ligula. Praesent aliquam vel est at ultrices. Nam semper, ex id ullamcorper sagittis, ligula purus consectetur nisi, vel cursus purus justo sit amet nisl. Vivamus auctor, elit vel finibus accumsan, elit ex vulputate quam, non vulputate est urna vel velit.',

    'Um projeto de sustentabilidade inovador da Universidade Q recebeu reconhecimento nacional. Os esforços para promover práticas ambientalmente responsáveis estão inspirando outras instituições a seguir o exemplo. Duis nec turpis ac urna dignissim consequat vel id dui. Curabitur vel dui id leo dignissim posuere.',

    'Estudantes brilhantes da Universidade R brilharam em uma competição internacional de ciências, destacando-se entre os melhores do mundo. Seu sucesso é um testemunho do rigor acadêmico da instituição. Curabitur sed quam sit amet dolor hendrerit posuere nec ut quam. Vivamus fringilla, risus id malesuada fermentum, risus mauris cursus quam, vel dapibus dui purus eu arcu.',

    'O Instituto S anunciou uma parceria emocionante com empresas locais para oferecer estágios remunerados. Essa colaboração proporcionará aos alunos experiências práticas e oportunidades de emprego após a formatura. Quisque sit amet egestas justo. Maecenas sed est vitae tortor bibendum mattis. In bibendum arcu vel justo efficitur, nec suscipit ligula dictum.',

    'A Universidade T inaugurou um novo laboratório de pesquisa equipado com tecnologia de ponta. Este centro de inovação impulsionará a descoberta científica e inspirará futuras gerações de pesquisadores. Integer nec turpis ac urna dignissim consequat vel id dui. Curabitur vel dui id leo dignissim posuere.',

    'ET Bilu, o famoso extraterrestre, revelou mensagens intrigantes na Universidade X. Os pesquisadores estão atônitos com as descobertas cósmicas, desencadeando uma nova era de exploração espacial e busca por vida alienígena. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
]

titulos_noticias = [
    "App Inovador",
    "Prêmio Internacional",
    "Evento Voluntariado",
    "Bolsas Estudo",
    "Robótica Avançada",
    "Sustentabilidade Reconhecimento",
    "Competição Ciências",
    "Parceria Estágios",
    "Laboratório Pesquisa",
    "ET Bilu",
]

def inserir_mock():
    conexao = conectardb()
    for i in range(len(noticias)):
        tupla = (titulos_noticias[i], 'Rene', random.randint(0, 2000), False, noticias[i])
        create_article_db(tupla, conexao)
    
    conexao.close()

# USAR SOMENTE QUANDO DESEJAR LIMPAR O BANCO
def deletar_tudo():
    con = psycopg2.connect(host='dpg-cl5v0ps72pts73af17m0-a.oregon-postgres.render.com', database='my_app_db_d3aj',
    user='my_app_user', password='MedlZen0ZlU6owtyW4AAPPsGijPvgfi8')

    sql = 'DELETE FROM noticia;'

    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def query_teste():
    conexao = conectardb()
    cur = conexao.cursor()
    sql = "SELECT * FROM noticia WHERE titulo = 'Testando novamente '"

    try:
        cur.execute(sql)
        result = cur.fetchall()
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        conexao.close()
    return 

def send_update_DB(usuario, old_title, news_title, content):
    conexao = conectardb()
    cur = conexao.cursor()

    sql = f"UPDATE noticia SET titulo = '{news_title}', corpo = '{content}' WHERE autor = '{usuario}' and titulo = '{old_title}'"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        conexao.close()
        return True
    return False

def get_last_comment_id():
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

def submit_comment_DB(title, comment, user):
    conexao = conectardb()
    cur = conexao.cursor()

    id = get_news_id_by_title(title)
    last_comment_id = get_last_comment_id()

    sql = f"INSERT INTO comentario (id, comentario, autor) VALUES ({id}, '{comment}', '{user}')"

    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        conexao.close()

def get_news_comments(title):
    conexao = conectardb()
    cur = conexao.cursor()

    id = get_news_id_by_title(title)

    query = f"SELECT * FROM comentario WHERE id = {id}"

    try:
        cur.execute(query)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        comments = cur.fetchall()
    cur.close()
    conexao.close()
    return comments

def upload_profile_pic_DB(user, imagem_bytes):
    conexao = conectardb()
    cur = conexao.cursor()

    try:
        cur.execute(f"UPDATE usuario SET profile_pic = %s WHERE nome_usuario = %s", (psycopg2.Binary(imagem_bytes), user))
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
    conexao.close()
    cur.close()



# query_teste()

# deletar_tudo()
# inserir_mock()


# querys uteis
# -- select * from noticia
# -- UPDATE noticia SET removida = False WHERE titulo = 'App Inovador';
# SELECT * FROM noticia WHERE autor = 'Laires';
# -- SELECT * FROM noticia WHERE titulo = 'Testeteste';
# -- DELETE FROM noticia WHERE titulo = 'Testeteste';