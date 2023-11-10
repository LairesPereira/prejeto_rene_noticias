# AUTORES MONIQUE E LAIRES
from lista_usuarios_cadastrados import ler_usuarios_cadastrados
from art import *
from flask import *
from dao import *

app = Flask(__name__)

login = False

adm_cadastrados = ler_usuarios_cadastrados('ADM')
usuarios_cadastrados = ler_usuarios_cadastrados('USUARIO')
usuario_logado = {}

# o sistema irá rodar até alguém ou algo interromper o programa
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

    sql = 'select * from adm_cadastrados'

    adm_cadastrados = get_users(sql, conexao)

    for adm in adm_cadastrados:
        if(login == adm[1] and senha == adm[2]):
            print(login, adm[1])
            print(senha, adm[2])
            return render_template('adm_logado.html', usuario=login)
        
    return render_template('login_page.html')

@app.route('/sing_up', methods=["POST"])
def create_user():
    name = str(request.form.get('txt'))
    password = str(request.form.get('pswd'))
    email = str(request.form.get('email'))

    conexao = conectardb()
    
    create = create_user_db(name, password, email, conexao)

    if create:
        return render_template('adm_logado.html')
    else:
        return render_template('login_page.html')
    
    


if __name__ == "__main__":
    app.run(debug=True)