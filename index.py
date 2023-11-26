# AUTORES MONIQUE E LAIRES
from flask import *
from flask_login import *
from dao import *
from decouple import config 
from warnin_colors import text_colors
from PIL import Image
from io import BytesIO
from parse_articles import parse_articles_to_download
import os

app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

@app.route('/')
def home():
    home_articles = get_articles_db()
    return render_template('home.html', articles=home_articles)

@app.route("/login_page")
def login_page():
    return render_template('login_page.html')
    
@app.route("/login", methods=["POST", "GET"])
def login():
    home_articles = get_articles_db()
    if 'usuario' in session:
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True)

    
    login = str(request.form.get('txt'))
    senha = str(request.form.get('pswd'))

    conexao = conectardb()

    sql = 'select * from usuario'

    usuarios = get_users(sql, conexao)

    for usuario in usuarios:
        username, password, full_name, cpf, is_adm, email, user_id, profile_pic, cidade, telefone, nascimento = usuario
        if(login == username and senha == password):
            session['usuario'] = login

            if is_adm:
                return render_template('adm_logado.html', usuario=login, articles=home_articles)
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

    if create:
        return render_template('usuario_logado.html')
    else:
        return render_template('login_page.html', sigun_up=sigun_up)

@app.route('/login/news')
def show_news_home():
    home_articles = get_articles_db()

    return jsonify(home_articles)
 
@app.route('/login/get_news/', methods=['GET'])
def read_new():
    news_title = request.args.get('news')
    article = read_article_db(news_title)
    return render_template('article.html', article=article[0], full_article=True, usuario=session['usuario'], show_comment_area=True)

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
    session.pop('usuario')
    return redirect('/')

@app.route('/delete_news_page/delete/', methods=['GET'])
def delete_news():
    news_title = request.args.get('news')
    delete = delete_article_db(news_title, session['usuario'])

    if delete:
        articles = get_user_articles(session['usuario'])
        return redirect('/delete_news_page')

@app.route('/delete_news_page', methods=['GET', 'DELETE'])
def delete_news_page():
    if 'usuario' in session:
        articles = get_user_articles(session['usuario'])
        return render_template('user_news.html', articles=articles, update_delete=True)

@app.route('/user_news')
def update_news_page():
    if 'usuario' in session:
        articles = get_user_articles(session['usuario'])
        print(articles)
        return render_template('user_news.html', articles=articles, update_delete=True)

@app.route('/update_news_page/', methods=['GET', 'POST'])
def update_news(): 
    if 'usuario' in session:
        title = request.args.get('news')

        article = get_article(title, session['usuario'])
        return render_template('update_news_page.html', article=article[0])
    
@app.route('/update_news_page/send_update/', methods=['POST'])
def send_update():
    if 'usuario' in session:
        old_title = request.form.get('old_title')
        title = request.form.get('news')
        content = request.form.get('content')

        update = send_update_DB(session['usuario'], old_title, title, content)
        
        if update:
            articles = get_article(title, session['usuario'])
            return redirect('user_news.html', articles=articles)
    
@app.route("/send_like", methods=['POST'])
def send_like():
    if 'usuario' in session:
        print(request.form)
        title = request.form.get('title')
        like = request.form.get('like')
        print(text_colors.FAIL + 'AQUI', title)
        like_insert = like_count_DB(title, like)
        home_articles = get_articles_db()
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True)

@app.route("/submit_comment", methods=['POST'])
def submit_comment():
    title = request.form.get('title')
    comment = request.form.get('comment')
    user = session['usuario']
    submit_comment_DB(title, comment, user)

@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get('search_news')
    match = search_DB(search)
    for i in match:
        print(i)
    return render_template('adm_logado.html', articles=match, show_more_btn=True)

@app.route("/user_profile", methods=["GET", "POST"])
def teste():
    user = session['usuario']
    user_info = get_user_info(user)
    return render_template('user_profile.html', user=user_info[0])

@app.route("/upload_profile_pic", methods=["POST"])
def upload_profile_pic():
    pic = request.files['profile-pic']
    img = pic.read()
    
    # Image.open(pic)
    # pixels = list(img.getdata())
    # hex_pixels = [f'{pixel[0]:02X}{pixel[1]:02X}{pixel[2]:02X}' for pixel in pixels]
    
    store_pic = upload_profile_pic_DB(session['usuario'], img)
    print(store_pic)

@app.route("/download_news", methods=["GET"])
def download_news():
    user = session['usuario']
    articles = get_user_articles(user)

    parsed_article_path = parse_articles_to_download(user, articles)
    
    # Deletar arquivos após serem enviados para downlad
    @after_this_request
    def remove_file(response):
        try:
            os.remove(parsed_article_path)
        except Exception as error:
            print(error)
        return response
    return send_file(parsed_article_path, as_attachment=True)





if __name__ == "__main__":
    app.run(debug=True)