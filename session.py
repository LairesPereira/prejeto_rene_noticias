from flask import session

def get_user_logged():
    print('teste session')
    if session['usuario']:
        return session['usuario'][0]
    return False

def user_isadm():
    if session['usuario'][1]:
        return True
    return False

def save_session(user: list):
    session['usuario'] = user