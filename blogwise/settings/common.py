import os
import logging

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

SESSION_COOKIE_NAME = 'blogwise'

# Logger Settings
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'blogwise.log'
LOGGING_LEVEL = logging.ERROR

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(DB_USER,
                                                            DB_PASSWORD,
                                                            DB_HOST,
                                                            DB_NAME)
DATABASE_URI = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
