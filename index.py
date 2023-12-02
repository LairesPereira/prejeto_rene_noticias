# AUTORES MONIQUE E LAIRES
from flask import *
from flask_login import *
from dao import *
from decouple import config 
from warnin_colors import text_colors
from PIL import Image
from io import BytesIO
from parse_articles import parse_articles_to_download
from random import randint
import os
import base64
from email_validator import validate_email, EmailNotValidError


app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

def validate_login(pswd, email):
    # validate password
    validate_result = [False, False, None]
    if len(pswd) > 6:
        for char in pswd:
            if char.isupper():
                validate_result[0] = True

    try:
        # Check that the email address is valid. Turn on check_deliverability
        # for first-time validations like on account creation pages (but not
        # login pages).
        emailinfo = validate_email(email, check_deliverability=False)
        validate_result[1] = True
        # After this point, use only the normalized form of the email address,
        # especially before going to a database query.
        email = emailinfo.normalized
    except EmailNotValidError as e:
        validate_result[2] = e
        # The exception message is human-readable explanation of why it's
        # not a valid (or deliverable) email address.

    return validate_result


def get_user_logged():
    if session['usuario']:
        return session['usuario'][0]

def user_isadm():
    if session['usuario'][1]:
        return True
    return False

def get_random_profile_pic():
    img_id = randint(1,5)
    path = f'static/avatars/Camada_{img_id}.jpg'
    img = Image.open(path).tobytes()
    return img

def get_profile_pics(articles):
    profile_pics = {}
    for article in articles:
        user_name = article[2]
        if not user_name in profile_pics:
            bin_pic = get_profile_pic_DB(user_name)
            print(bin_pic)
            print(type(bin_pic))
            if bin_pic:
                converted_pic = base64.b64encode(bytes(bin_pic[0][0])).decode('utf-8')
                profile_pics[user_name] = converted_pic

    return profile_pics

@app.route('/')
def home():
    home_articles = get_articles_db()
    profile_pics = get_profile_pics(home_articles)
    return render_template('home.html', articles=home_articles, profile_pic=profile_pics)

@app.route("/login_page")
def login_page():
    return render_template('login_page.html')
    
@app.route("/login", methods=["POST", "GET"])
def login():
    home_articles = get_articles_db()

    if 'usuario' in session and session['usuario'][1]:
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), adm_options=True)

    login = str(request.form.get('txt'))
    senha = str(request.form.get('pswd'))

    usuario = get_users(login, senha )
    if usuario:
        is_adm = usuario[0][4]

        session['usuario'] = [login, is_adm]
        print(session)
        if is_adm:
            return render_template('adm_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), adm_options=True)
        return render_template('usuario_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), show_more_btn=True )
        
    return render_template('login_page.html', login_fail=True)

@app.route('/sing_up', methods=["POST"])
def create_user():
    name = str(request.form.get('txt'))
    password = str(request.form.get('pswd'))
    email = str(request.form.get('email'))
    validate_credentials = validate_login(password, email)
    isadm_val = request.form.get('isadm')
    isadm = True if isadm_val == 'on' else False
    home_articles = get_articles_db()

    profile_pics = get_profile_pics(home_articles)

    conexao = conectardb()
    
    if not validate_credentials[0] or validate_credentials[1]:
        print('nao passou')
        return render_template('login_page.html', sigun_up=False)
    
    print(name, password, email, conexao, isadm)
    create = create_user_db(name, password, email, conexao, isadm)
    print(create)
    if create[0]:
        return render_template('login_page.html', sigun_up=False)
    if create[1] and isadm:
        session['usuario'] = [name, isadm]
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, adm_options=True, profile_pic=profile_pics)
    if create[1] and isadm == False:
        session['usuario'] = [name, isadm]
        return render_template('usuario_logado.html', articles=home_articles, profile_pic=profile_pics, show_more_btn=True)
    

@app.route('/login/news')
def show_news_home():
    home_articles = get_articles_db()

    return jsonify(home_articles)
 
@app.route('/login/get_news/', methods=['GET'])
def read_new():
    news_title = request.args.get('news')
    article = read_article_db(news_title)
    profile_pics = get_profile_pics(article)
    comments = get_news_comments(news_title)
    if session['usuario'][1]:
        return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, show_comments=comments, profile_pic=profile_pics, adm_options=True)
    return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, profile_pic=profile_pics)

@app.route('/create_news', methods=['GET', 'POST'])
def create_news():
    if request.method == 'POST':
        titulo = str(request.form.get('titulo'))
        texto = str(request.form.get('textarea'))
        
        conexao = conectardb()
        news_info = (titulo, get_user_logged(), 0, False, texto)

        create_article_db(news_info, conexao)

        return render_template('create_news.html', adm_options=True)
    else: 
        return render_template('create_news.html', adm_options=True)

@app.route('/logOut', methods=['GET'])
def logout():
    if 'usuario' in session:
        session.clear()
    return redirect('/')

@app.route('/delete_news_page/delete/', methods=['GET'])
def delete_news():
    news_title = request.args.get('news')
    delete = delete_article_db(news_title, get_user_logged())

    if delete:
        articles = get_user_articles(get_user_logged())
        return redirect('/delete_news_page')

@app.route('/delete_news_page', methods=['GET', 'DELETE'])
def delete_news_page():
    if 'usuario' in session and session['usuario'][1]:
        articles = get_user_articles(get_user_logged())
        profile_pics = get_profile_pics(articles)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)

@app.route('/user_news')
def update_news_page():
    if 'usuario' in session and session['usuario'][1]:
        articles = get_user_articles(get_user_logged())
        profile_pics = get_profile_pics(articles)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)

@app.route('/update_news_page/', methods=['GET', 'POST'])
def update_news(): 
    if 'usuario' in session:
        title = request.args.get('news')

        article = get_article(title, get_user_logged())
        return render_template('update_news_page.html', article=article[0])
    
@app.route('/update_news_page/send_update/', methods=['POST'])
def send_update():
    if 'usuario' in session:
        old_title = request.form.get('old_title')
        title = request.form.get('news')
        content = request.form.get('content')

        update = send_update_DB(get_user_logged(), old_title, title, content)
        
        if update:
            articles = get_article(title, get_user_logged())
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
    user = get_user_logged()

    submit_comment_DB(title, comment, user)

    article = read_article_db(title)
    profile_pics = get_profile_pics(article)
    comments = get_news_comments(title)
    
    return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, show_comments=comments, profile_pic=profile_pics, adm_options=user_isadm())

@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get('search_news')
    match = search_articles_DB(search)
    profile_pics = get_profile_pics(match)
    return render_template('adm_logado.html', articles=match, show_more_btn=True, profile_pic=profile_pics, adm_options=user_isadm() )

@app.route("/user_profile", methods=["GET", "POST"])
def teste():
    user = get_user_logged()
    user_info = get_user_info(user)
    print(user_info)
    # decode binary image from db to base64
    image_base64 = base64.b64encode(bytes(user_info[0][7])).decode('utf-8') 
    
    return render_template('user_profile.html', user=user_info[0], profile_pic=image_base64, adm_options=user_isadm())

@app.route("/upload_profile_pic", methods=["POST"])
def upload_profile_pic():
    user = get_user_logged()
    print(request.files['profile-pic'])
    img = request.files['profile-pic'].read()
    upload_profile_pic_DB(user, img)

    return redirect('/user_profile')

@app.route("/download_news", methods=["GET"])
def download_news():
    user = get_user_logged()
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