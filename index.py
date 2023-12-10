# AUTORES MONIQUE E LAIRES
from flask import *
from flask_login import *
from dao import *
from decouple import config 
from auth import *
from articles import *
from user import *
from interactions import *
from utils import *

app = Flask(__name__)
app.secret_key = config("SECRET_KEY")

# auth routes
app.register_blueprint(auth_blueprint, url_prefix='/login')

# articles routes
app.register_blueprint(getnews_blueprint, url_prefix='/login/get_news/')
app.register_blueprint(usernews_blueprint, url_prefix='/user_news')
app.register_blueprint(createnews_blueprint, url_prefix='/create_news')
app.register_blueprint(deletenewspage_delete, url_prefix='/delete_news_page/delete/')
app.register_blueprint(updatenewspage_sendupdate, url_prefix='/update_news_page/send_update/')

# user routes
app.register_blueprint(uploadprofilepic, url_prefix='/upload_profile_pic')
app.register_blueprint(updateprofile, url_prefix='/update_profile')
app.register_blueprint(signup_blueprint, url_prefix='/sign_up')
app.register_blueprint(logout_bluprint, url_prefix='/logOut')

# interactions routes
app.register_blueprint(sendlike_blueprint, url_prefix='/send_like')
app.register_blueprint(submitcomment_blueprint, url_prefix='/submit_comment')
app.register_blueprint(downloadnews_blueprint, url_prefix='/download_news')

# main pages
@app.route('/')
def home():
    conexao = conectardb()
    home_articles = get_articles_db(conexao)
    profile_pics = get_profile_pics(home_articles, conexao)
    close_conection(conexao)
    return render_template('home.html', articles=home_articles, profile_pic=profile_pics)

@app.route('/delete_news_page', methods=['GET', 'DELETE'])
def delete_news_page():
    if get_user_logged() and user_isadm():
        conexao = conectardb()
        articles = get_user_articles(get_user_logged(), conexao)
        profile_pics = get_profile_pics(articles, conexao)
        close_conection(conexao)
        return render_template('user_news.html', articles=articles, update_delete=True, profile_pic=profile_pics, adm_options=True)

@app.route('/update_news_page/', methods=['GET', 'POST'])
def update_news(): 
    if get_user_logged():
        title = request.args.get('news')
        article = get_article(title, get_user_logged())
        return render_template('update_news_page.html', article=article[0])
    
@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get('search_news')
    # find all articles that match with the search request from user
    conexao = conectardb()
    match = search_articles_DB(search, conexao)
    profile_pics = get_profile_pics(match, conexao)
    articles_user_likes = articles_user_like(get_user_logged(), conexao)
    conexao.close()
    return render_template('adm_logado.html', articles=match, show_more_btn=True, profile_pic=profile_pics, adm_options=user_isadm(), user_likes=articles_user_likes)

@app.route("/user_profile", methods=["GET", "POST"])
def teste():
    user = get_user_logged()
    user_info = get_user_info(user)
    
    # recieve a base64 string that represents user profile picture
    image_base64 = user_info[0][7] 
    # image_base64 = 'laires'
    return render_template('user_profile.html', user=user_info[0], profile_pic=image_base64, adm_options=user_isadm())

if __name__ == "__main__":
    app.run(debug=True)