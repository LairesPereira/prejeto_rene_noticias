import psycopg2
# from datetime import datetime
from decouple import config

def conectardb():
    con = psycopg2.connect(
        host=config("HOST_DATABASE"),
        database=config("DATABASE_NAME"),
        user=config("DATABASE_USER"),
        password=config("DATABASE_PASS")
    )

    return con

def get_users(sql, conexao): 
    cur = conexao.cursor()

    try:
        cur.execute(sql)
        adms_list = cur.fetchall()
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.close()

    return adms_list

def create_user_db(name, password, email, conexao):
    cur = conexao.cursor()
    
    query_check_email_exists= f"SELECT COUNT(*) AS total FROM usuario WHERE nome_usuario = '{name}' OR email = '{email}';"

    search_result = 0
    try:
        cur.execute(query_check_email_exists)
        fetch = cur.fetchall()
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        search_result = fetch[0][0]

    if search_result == 0:
        last_id_query = "SELECT * FROM usuario ORDER BY id DESC LIMIT 1;"

        cur.execute(last_id_query)

        last_id = cur.fetchall()

        sql = f"insert into usuario values ({last_id[0][0] + 1}, '{name}', '{password}', null, null, 'false', '{email}')"
        
        try:
            cur.execute(sql)
        except psycopg2.IntegrityError:
            conexao.rollback()
        else:
            conexao.commit()
            search_result = 1

        conexao.close()
        return search_result

def create_article_db(sql, conexao):
    cur = conexao.cursor()

    # Insrir uma noticia no Banco
    # sql = f"insert into news_table values (1, 'minha primeira noticia', 'laires', 'este eh o corpo da noticia', 232, false)"
    sucess = False
    try:
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
        sucess = True
    # conexao.close()
    return sucess

def get_articles_db(conexao): 
    cur = conexao.cursor()
    cur.execute('select * from news_table')
    recset = cur.fetchall()
    conexao.close()
    return recset

def read_article_db(title, conexao):
    cur = conexao.cursor()

    sql = f"SELECT * FROM news_table WHERE  titulo = '{title}' "

    try:
        cur.execute(sql)
        article = cur.fetchall()
    except psycopg2.IntegrityError:
        conexao.rollback()
    else:
        conexao.commit()
    
    conexao.close()
    
    return article

# con = conectardb()
# create_user_db('laires', '123', 'lairesspsoares@gmail.com', con)

# mock de noticias para inserir no DB
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
        print(i)
        sql = f"insert into news_table values ('1', '{titulos_noticias[i]}', 'laires', '{noticias[i]}', 232, false)"
        create_article_db(sql, conexao)
    conexao.close()

# USAR SOMENTE QUANDO DESEJAR LIMPAR O BANCO
def deletar_tudo():
    con = psycopg2.connect(host='dpg-cl5v0ps72pts73af17m0-a.oregon-postgres.render.com', database='my_app_db_d3aj',
    user='my_app_user', password='MedlZen0ZlU6owtyW4AAPPsGijPvgfi8')

    sql = 'DELETE FROM news_table;'

    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

# deletar_tudo()
# inserir_mock()
