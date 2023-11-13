# AUTORES MONIQUE E LAIRES
from lista_usuarios_cadastrados import ler_usuarios_cadastrados
import secrets
from flask import *
from flask_login import *
from dao import *
from decouple import config 


app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

@app.route('/')
def home():
    conexao = conectardb()

    home_articles = get_articles_db(conexao)

    return render_template('home.html', articles=home_articles)

@app.route("/login_page")
def login_page():
    return render_template('login_page.html')
    
@app.route("/login", methods=["POST"])
def login():
    login = str(request.form.get('txt'))
    senha = str(request.form.get('pswd'))

    conexao = conectardb()

    sql = 'select * from usuario'

    usuario = get_users(sql, conexao)

    for usuario in usuario:
        if(login == usuario[1] and senha == usuario[2]):
            session['usuario'] = login
            print(session['usuario'], login)
            if usuario[5]:
                return render_template('adm_logado.html', usuario=login)
            return render_template('usuario_logado.html', usuario=login)
        
    return render_template('login_page.html')

@app.route('/sing_up', methods=["POST"])
def create_user():
    name = str(request.form.get('txt'))
    password = str(request.form.get('pswd'))
    email = str(request.form.get('email'))

    conexao = conectardb()
    
    create = create_user_db(name, password, email, conexao)
    sigun_up = True if create == 1 else False
    print(create, sigun_up)
    if create:
        return render_template('usuario_logado.html')
    else:
        return render_template('login_page.html', sigun_up=sigun_up)

@app.route('/login/news')
def show_news_home():
    conexao = conectardb()

    home_articles = get_articles_db(conexao)

    return jsonify(home_articles)

    
@app.route('/login/get_news/', methods=['GET'])
def read_new():
    news_title = request.args.get('news')
    
    conexao = conectardb()
    article = read_article_db(news_title, conexao)
    print(article)
    return render_template('article.html', article=article)

@app.route('/create_news', methods=['GET', 'POST'])
def create_news():
    if request.method == 'POST':
        print(request.form)
        titulo = str(request.form.get('titulo'))
        texto = str(request.form.get('textarea'))
        
        conexao = conectardb()

        sql = f"INSERT INTO news_table VALUES (1, '{titulo}', 'laires', '{texto}', 233, false )"

        create_article_db(sql, conexao)

        return render_template('create_news.html')
    else: 
        print('aqui')
        return render_template('create_news.html')

if __name__ == "__main__":
    app.run(debug=True)