# AUTORES MONIQUE E LAIRES
from lista_usuarios_cadastrados import ler_usuarios_cadastrados
from flask import *
from flask_login import *
from dao import *
from decouple import config 


app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

@app.route('/')
def home():
    print('aqui de novo')
    conexao = conectardb()

    home_articles = get_articles_db(conexao)
    print(home_articles)
    return render_template('home.html', articles=home_articles)

@app.route("/login_page")
def login_page():
    return render_template('login_page.html')
    
@app.route("/login", methods=["POST", "GET"])
def login():
    print(session)
    if 'usuario' in session:
        print(session['usuario'])
        return render_template('adm_logado.html')

    
    login = str(request.form.get('txt'))
    senha = str(request.form.get('pswd'))

    conexao = conectardb()

    sql = 'select * from usuario'

    usuarios = get_users(sql, conexao)

    for usuario in usuarios:
        username, password, full_name, cpf, is_adm, email, user_id = usuario
        print('aqui')
        print(usuario)
        if(login == username and senha == password):
            session['usuario'] = login
            print(session['usuario'], login)
            if is_adm:
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
        titulo = str(request.form.get('titulo'))
        texto = str(request.form.get('textarea'))
        
        conexao = conectardb()
        news_info = (titulo, session['usuario'], 0, False, texto)

        create_article_db(news_info, conexao)

        return render_template('create_news.html')
    else: 
        return render_template('create_news.html')

@app.route('/logOut', methods=['GET'])
def logout():
    print(session['usuario'])
    session.pop('usuario')

    conexao = conectardb()

    home_articles = get_articles_db(conexao)

    return redirect('/')



if __name__ == "__main__":
    app.run(debug=True)