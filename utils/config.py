
from utils.functions import get_sqlalchemy_uri
from utils.settings import DATABASE

class Conf():
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri(DATABASE=DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPYION = False
    SECRET_KEY = '1212'