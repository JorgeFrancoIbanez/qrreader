import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'Add-your-secret-here'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/col'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
