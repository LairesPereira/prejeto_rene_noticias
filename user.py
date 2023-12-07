from flask import *
from session import *
from dao import *
from utils import *

uploadprofilepic = Blueprint('uploadprofilepic', __name__)
updateprofile = Blueprint('updateprofile', __name__)

@uploadprofilepic.route('', methods=["POST"])
def upload_profile_pic():
    user = get_user_logged()
    # we read the raw file send by the user and we convert to a base64 string
    img = request.files['profile-pic'].read()
    img = base64.b64encode(img).decode('utf-8')

    # save image in a text field on DB
    upload_profile_pic_DB(user, img)

    return redirect('/user_profile')

@updateprofile.route('', methods=["POST"])
def update_profile():
    full_name = request.form.get('full-name')
    city = request.form.get('city')
    phone = request.form.get('phone')
    birthday = request.form.get('birthday')
    
    home_articles = get_articles_db()
    
    update_profile_BD(get_user_logged(), full_name, city, phone, birthday)

    if get_user_logged() and user_isadm():
        likes = articles_user_like(get_user_logged())
        return render_template('adm_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), adm_options=True, user_likes=likes)

    if get_user_logged() and user_isadm() == False:
        likes = articles_user_like(get_user_logged())
        print(likes)
        return render_template('usuario_logado.html', articles=home_articles, show_more_btn=True, profile_pic=get_profile_pics(home_articles), user_likes=likes)       
