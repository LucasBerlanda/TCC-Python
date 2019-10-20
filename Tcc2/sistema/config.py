import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'essa-e-chave-secreta'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/tcc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    Degug=True

    POSTS_PER_PAGE = 8
