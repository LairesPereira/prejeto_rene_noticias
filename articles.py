from flask import *
from session import *
from dao import *
from utils import *

getnews_blueprint = Blueprint('get_news', __name__)
usernews_blueprint = Blueprint('user_news', __name__)
createnews_blueprint = Blueprint('create_news', __name__)
deletenewspage_delete = Blueprint('deletenewspage_delete', __name__)
updatenewspage_sendupdate = Blueprint('updatenewspage_sendupdate', __name__)

@getnews_blueprint.route('', methods=['GET'])
def read_new():
    news_title = request.args.get('news')
    # load page content
    conexao = conectardb()
    article = read_article_db(news_title, conexao)
    profile_pics = get_profile_pics(article, conexao)
    comments = get_news_comments(news_title, conexao)
    likes_tuple = get_news_likes(news_title, conexao)
    articles_user_likes = articles_user_like(get_user_logged(), conexao)
    conexao.close()
    
    # parse news likes to one list of strings
    likes_strings = []
    for like in likes_tuple:
        likes_strings.append(like[0])
    likes = ", ".join(likes_strings)

    if user_isadm():
        return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, show_comments=comments, profile_pic=profile_pics, adm_options=True, user_likes=articles_user_likes, show_likes=likes, show_creation_date=True)
    return render_template('article.html', article=article[0], full_article=True, usuario=get_user_logged(), show_comment_area=True, profile_pic=profile_pics, user_likes=articles_user_likes, show_creation_date=True)

# enviar de volta para index
@usernews_blueprint.route('')
def update_news_page():
    if get_user_logged() and user_isadm():
        conexao = conectardb()
        articles = get_user_articles(get_user_logged(), conexao)
        print(articles)
        profile_pics = get_profile_pics(articles, conexao, get_user_logged())
        close_conection(conexao)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)
    
@createnews_blueprint.route('', methods=['GET', 'POST'])
def create_news():
    if request.method == 'POST':
        titulo = str(request.form.get('titulo'))
        texto = str(request.form.get('textarea'))
        
        conexao = conectardb()
        check_title_exists = check_news_title_exists(titulo, conexao)

        bad_chars = [';', ':', '!', "*", "'", '#']
        titulo = ''.join(i for i in titulo if not i in bad_chars)
        # shapes the article info
        news_info = (titulo, get_user_logged(), 0, False, texto, 0)
                
        # dont allow create article if title already exists
        if check_title_exists:
            close_conection(conexao)
            return render_template('create_news.html', adm_options=True, alert=True)
    
        create_article_db(news_info, conexao)
        close_conection(conexao)
        return render_template('create_news.html', adm_options=True)
    
    # renders the same page in case of any problem with request
    return render_template('create_news.html', adm_options=True)
    
@deletenewspage_delete.route('', methods=["GET"])
def delete_news():
    news_title = request.args.get('news')

    conexao = conectardb()
    # delete article only if belongs to the user in session
    delete = delete_article_db(news_title, get_user_logged(), conexao)

    if delete:
        articles = get_user_articles(get_user_logged(), conexao)
        close_conection(conexao)
        return redirect('/delete_news_page')

@updatenewspage_sendupdate.route('', methods=["POST"])
def send_update():
    if get_user_logged():
        # get old title for search in DB
        old_title = request.form.get('old_title')
        # new title and content for update
        title = request.form.get('news')
        content = request.form.get('content')
        conexao = conectardb()
        update = send_update_DB(get_user_logged(), old_title, title, content, conexao)
        
        if update:
            close_conection(conexao)
            return redirect('user_news.html')