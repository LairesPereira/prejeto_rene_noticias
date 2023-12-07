from flask import *
from session import *
from dao import *
from utils import *
from email_validator import validate_email, EmailNotValidError

auth_blueprint = Blueprint('login', __name__)
signup_blueprint = Blueprint('sign_up', __name__)
logout_bluprint = Blueprint('logut', __name__)

@auth_blueprint.route('/', methods=["GET", "POST"])
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

        save_session([login, is_adm])
        if is_adm:
            return render_template('adm_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), adm_options=True, user_likes=articles_user_like(get_user_logged()))
        return render_template('usuario_logado.html', usuario=login, articles=home_articles, profile_pic=get_profile_pics(home_articles), show_more_btn=True )
        
    return render_template('login_page.html', login_fail=True)


@signup_blueprint.route('', methods=["POST"])
def create_user():
    name = str(request.form.get('txt'))
    password = str(request.form.get('pswd'))
    email = str(request.form.get('email'))
    isadm_val = request.form.get('isadm')

    isadm = True if isadm_val == 'on' else False

    validate_credentials = validate_login(password, email) # check format
    
    home_articles = get_articles_db()
    profile_pics = get_profile_pics(home_articles)
    
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

@logout_bluprint.route('', methods=["GET"])
def logout():
    # clear session
    if get_user_logged():
        session.clear()
    return redirect('/')


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