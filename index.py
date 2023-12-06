# AUTORES MONIQUE E LAIRES
from flask import *
from flask_login import *
from dao import *
from decouple import config 
from warnin_colors import text_colors
from PIL import Image
from parse_articles import parse_articles_to_download
from downloadPDF import text_to_pdf
from random import randint
import os
import base64
from email_validator import validate_email, EmailNotValidError
from crudUser import *
from utils import *

app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

def get_user_logged():
    if session['usuario']:
        return session['usuario'][0]
    return False

def user_isadm():
    if session['usuario'][1]:
        return True
    return False

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

    if 'usuario' in session and user_isadm():
        likes = articles_user_like(get_user_logged())
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), adm_options=True, user_likes=likes)

    if 'usuario' in session and user_isadm() == False:
        likes = articles_user_like(get_user_logged())
        return render_template('usuario_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), user_likes=likes)       

    login = str(request.form.get('txt'))
    senha = str(request.form.get('pswd'))

    usuario = get_users(login, senha )
    if usuario:
        is_adm = usuario[0][4]

        session['usuario'] = [login, is_adm]
        if is_adm:
            return render_template('adm_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), adm_options=True, user_likes=articles_user_like(get_user_logged()))
        return render_template('usuario_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), show_more_btn=True )
        
    return render_template('login_page.html', login_fail=True)

@app.route('/sing_up', methods=["POST"])
def create_user():
    # get request user info
    name = str(request.form.get('txt'))
    password = str(request.form.get('pswd'))
    email = str(request.form.get('email'))
    
    isadm_val = request.form.get('isadm')
    isadm = True if isadm_val == 'on' else False

    validate_credentials = validate_login(password, email) # check format
    home_articles = get_articles_db()
    profile_pics = get_profile_pics(home_articles)
    
    # check password format
    if validate_credentials[0] == False:
        return render_template('login_page.html', sigun_up='A senha deve ter formato "Senha1"')
    
    # only try create user if credentials are valid
    create = create_user_db(name, password, email, isadm) 
    
    # succes creating adm
    if create[0] == False and create[1] == True and isadm == True: 
        session['usuario'] = [name, isadm]
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, adm_options=True, profile_pic=profile_pics, user_likes=articles_user_like(get_user_logged()))
    
    # fail creating any user
    if create[0] == True and create[1] == False: 
        return render_template('login_page.html', sigun_up='Usuario ou Email já cadastrados')
    
    # sucess creating regular user
    if create[1] and isadm == False:
        session['usuario'] = [name, isadm]
        return render_template('usuario_logado.html', articles=home_articles, profile_pic=profile_pics, show_more_btn=True)
    
    # case any other error
    return render_template('login_page.html', sigun_up='Erro no cadastro')

@app.route('/login/get_news/', methods=['GET'])
def read_new():
    # get request info
    news_title = request.args.get('news')
    
    # load page content
    article = read_article_db(news_title)
    profile_pics = get_profile_pics(article)
    comments = get_news_comments(news_title)
    likes_tuple = get_news_likes(news_title)
    
    # parse news likes to one list of strings
    likes_strings = []
    for like in likes_tuple:
        likes_strings.append(like[0])
    likes = ", ".join(likes_strings)

    if user_isadm():
        return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, show_comments=comments, profile_pic=profile_pics, adm_options=True, user_likes=articles_user_like(get_user_logged()), show_likes=likes, show_creation_date=True)
    return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, profile_pic=profile_pics, user_likes=articles_user_like(get_user_logged()), show_creation_date=True)

@app.route('/create_news', methods=['GET', 'POST'])
def create_news():
    if request.method == 'POST':
        # get request info
        titulo = str(request.form.get('titulo'))
        texto = str(request.form.get('textarea'))

        check_title_exists = check_news_title_exists(titulo)

        # shapes the article info
        news_info = (titulo, get_user_logged(), 0, False, texto, 0)
                
        # dont allow create article if title already exists
        if check_title_exists:
            return render_template('create_news.html', adm_options=True, alert=True)
    
        create_article_db(news_info)
        return render_template('create_news.html', adm_options=True)
    
    # renders the same page in case of any problem with request
    return render_template('create_news.html', adm_options=True)
    

@app.route('/logOut', methods=['GET'])
def logout():
    # clear session
    if get_user_logged():
        session.clear()
    return redirect('/')

@app.route('/delete_news_page/delete/', methods=['GET'])
def delete_news():
    news_title = request.args.get('news')

    # delete article only if belongs to the user in session
    delete = delete_article_db(news_title, get_user_logged())

    if delete:
        articles = get_user_articles(get_user_logged())
        return redirect('/delete_news_page')

@app.route('/delete_news_page', methods=['GET', 'DELETE'])
def delete_news_page():
    if get_user_logged() and user_isadm():
        articles = get_user_articles(get_user_logged())
        profile_pics = get_profile_pics(articles)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)

@app.route('/user_news')
def update_news_page():
    if get_user_logged() and user_isadm():
        articles = get_user_articles(get_user_logged())
        profile_pics = get_profile_pics(articles)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)

@app.route('/update_news_page/', methods=['GET', 'POST'])
def update_news(): 
    if get_user_logged():
        title = request.args.get('news')

        article = get_article(title, get_user_logged())
        return render_template('update_news_page.html', article=article[0])
    
@app.route('/update_news_page/send_update/', methods=['POST'])
def send_update():
    if get_user_logged():
        # get old title for search in DB
        old_title = request.form.get('old_title')
        # new title and content for update
        title = request.form.get('news')
        content = request.form.get('content')

        update = send_update_DB(get_user_logged(), old_title, title, content)
        
        if update:
            articles = get_article(title, get_user_logged())
            return redirect('user_news.html', articles=articles)
    
@app.route("/send_like", methods=['POST'])
def send_like():
    if get_user_logged():
        title = request.form.get('title')
        
        # like is boolean so we can toggle the query string on DB
        like = request.form.get('like')
        user = get_user_logged()
        
        like_count_DB(title, like, user)
        home_articles = get_articles_db()
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True)

@app.route("/submit_comment", methods=['POST'])
def submit_comment():    
    # get request info
    title = request.form.get('title')
    comment = request.form.get('comment')
    
    user = get_user_logged()

    submit_comment_DB(title, comment, user)
    update_total_comment(title)

    # load article content to display it on full article page    
    article = read_article_db(title)
    profile_pics = get_profile_pics(article)    
    comments = get_news_comments(title)
    likes_tuple = get_news_likes(title)

    # We make a list with the names of users who liked the current article
    likes_strings = []
    for like in likes_tuple:
        likes_strings.append(like[0])
    likes = ", ".join(likes_strings)

    
    return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, show_comments=comments, profile_pic=profile_pics, adm_options=user_isadm(), user_likes=articles_user_like(get_user_logged()), show_likes=likes, show_creation_date=True)

@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get('search_news')
    # find all articles that match with the search request from user
    match = search_articles_DB(search)
    profile_pics = get_profile_pics(match)
    return render_template('adm_logado.html', articles=match, show_more_btn=True, profile_pic=profile_pics, adm_options=user_isadm(), user_likes=articles_user_like(get_user_logged()))

@app.route("/user_profile", methods=["GET", "POST"])
def teste():
    user = get_user_logged()
    user_info = get_user_info(user)
    
    # recieve a base64 string that represents user profile picture
    image_base64 = user_info[0][7] 
    
    return render_template('user_profile.html', user=user_info[0], profile_pic=image_base64, adm_options=user_isadm())

@app.route("/upload_profile_pic", methods=["POST"])
def upload_profile_pic():
    user = get_user_logged()
    # we read the raw file send by the user and we convert to a base64 string
    img = request.files['profile-pic'].read()
    img = base64.b64encode(img).decode('utf-8')

    # save image in a text fild on DB
    upload_profile_pic_DB(user, img)

    return redirect('/user_profile')

@app.route("/download_news", methods=["GET"])
def download_news():
    # laod all articles from the current user
    user = get_user_logged()
    articles = get_user_articles(user)

    # create a txt with articles info from DB and return the path
    parsed_article_path = parse_articles_to_download(user, articles)
    
    # read txt file
    file = open(parsed_article_path)
    text = file.read()
    file.close()

    # convert it to .PDF
    text_to_pdf(text, f'{user}.pdf')

    # When the request is ready to be finished we delete the .txt and .PDF files from server
    @after_this_request
    def remove_file(response):
        try:
            os.remove(parsed_article_path)
            os.remove(f'{user}.pdf')
        except Exception as error:
            print(error)
        return response
    return send_file(f'{user}.pdf', as_attachment=True)

@app.route('/update_profile', methods=["POST"])
def update_profile():
    # get request info
    full_name = request.form.get('full-name')
    city = request.form.get('city')
    phone = request.form.get('phone')
    birthday = request.form.get('birthday')
    
    home_articles = get_articles_db()
    # update profile 
    update_profile_BD(get_user_logged(), full_name, city, phone, birthday)

    # return ADM template
    if get_user_logged()and user_isadm():
        likes = articles_user_like(get_user_logged())
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), adm_options=True, user_likes=likes)

    # return user template
    if get_user_logged() and user_isadm() == False:
        likes = articles_user_like(get_user_logged())
        print(likes)
        return render_template('usuario_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), user_likes=likes)       

if __name__ == "__main__":
    app.run(debug=True)