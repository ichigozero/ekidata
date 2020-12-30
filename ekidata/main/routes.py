from ekidata.main import bp


@bp.route('/', defaults={'path': ''})
@bp.route('/<string:path>')
@bp.route('/<path:path>')
def catch_all(path):
    return bp.send_static_file('index.html')
