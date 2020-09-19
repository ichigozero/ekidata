import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or ''.join(['sqlite:///', os.path.join(basedir, 'ekidata.db')])
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
