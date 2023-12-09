from flask import *
from session import *
from dao import *
from utils import *
from downloadPDF import text_to_pdf
from parse_articles import parse_articles_to_download
import os

sendlike_blueprint = Blueprint('sendlike_blueprint', __name__)
submitcomment_blueprint = Blueprint('submitcomment_blueprint', __name__)
downloadnews_blueprint = Blueprint('downloadnews_blueprint', __name__)

@sendlike_blueprint.route('', methods=["POST"])
def send_like():
    if get_user_logged():
        title = request.form.get('title')
    
        # like is boolean so we can toggle the query string on DB
        like = request.form.get('like')
        user = get_user_logged()
        
        conexao = conectardb()

        like_count_DB(title, like, user, conexao)
        home_articles = get_articles_db(conexao)
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True)
    
@submitcomment_blueprint.route('', methods=["POST"])
def submit_comment():    
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

@downloadnews_blueprint.route('', methods=["GET"])
def download_news():
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