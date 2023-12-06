from dao import *

def get_profile_pics(articles):
    profile_pics = {}
    for article in articles:
        user_name = article[2]
        if not user_name in profile_pics:
            print('not in dic')
            bin_pic = get_profile_pic_DB(user_name)
            profile_pics[user_name] = bin_pic[0][0]
    return profile_pics