import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123@127.0.0.1:5432/myblog' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 3