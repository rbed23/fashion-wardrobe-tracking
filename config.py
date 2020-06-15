import os
from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))
_db_name = os.environ['MYSQL_DATABASE']
_db_user = os.environ['MYSQL_DB_USER']
_db_pass = os.environ['MYSQL_DB_PASS']
sql3db = os.environ['SQLITE3_DB']

class BaseConfiguration(object):
    HASH_ROUNDS = 100000
    SECRET_KEY = 'flask-session-insecure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql://' +\
                                _db_user + ':' +\
                                _db_pass + '@' +\
                                'localhost' + '/' +\
                                _db_name
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, sql3db)
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False



class DevelopmentConfig(BaseConfiguration):
    DEBUG = True
    ENV = 'Development'
    ERROR_LOG_PATH = 'errors_log_dev.txt'



class Test(BaseConfiguration):
    DEBUG = False
    ENV = "Testing"
    ERROR_LOG_PATH = 'errors_log_testing.txt'
    HASH_ROUNDS = 1000
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # + join(_cwd, 'testing.db')
    TESTING = True



class ProductionConfig(BaseConfiguration):
    ENV = "Production"
    ERROR_LOG_PATH = 'errors_log_production.txt'