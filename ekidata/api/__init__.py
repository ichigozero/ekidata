from flask import Blueprint

bp = Blueprint('api', __name__)

from ekidata.api import version_1, version_2
