from .common import *

ENV = 'development'
SECRET_KEY = 'secretzzzzz'
DEBUG = True

SESSION_COOKIE_NAME = 'blogwise'
# EXPLAIN_TEMPLATE_LOADING = True

LOGGING_LEVEL = logging.INFO

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'xotomajor')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'admin')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'blogwise')
DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(DB_USER,
                                                 DB_PASSWORD,
                                                 DB_HOST,
                                                 DB_NAME)
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

print('Dev settings loaded.')
