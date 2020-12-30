from flask import Blueprint

bp = Blueprint(
    'main',
    __name__,
    static_folder='../../../build',
    static_url_path='/'
)

from ekidata.main import routes