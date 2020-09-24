from flask import Blueprint
from flask import abort
from sqlalchemy.orm import aliased

from ekidata import db
from ekidata import mongo
from ekidata.models import ConnectingStation
from ekidata.models import Line
from ekidata.models import Station

bp = Blueprint('routes', __name__)


@bp.route(
    '/ekidata/api/v1.0/prefectures/<int:prefecture_id>/lines',
    methods=['GET']
)
def get_lines(prefecture_id):
    rows = db.session.query(
        Line.id,
        Line.common_name,
        Line.status,
        Line.sort_code,
        Station.prefecture_id
    ).join(
        Line,
        Line.id == Station.line_id,
        isouter=True
    ).filter(
        Station.prefecture_id == prefecture_id,
        Station.status == 0,
        Station.line_id > 10000
    ).order_by(
        Line.status,
        Line.id
    ).distinct().all()

    if len(rows) == 0:
        abort(404)

    lines = []

    for row in rows:
        line = {
            'id': row.id,
            'common_name': row.common_name
        }
        lines.append(line)

    return {'lines': lines}


@bp.route(
    '/ekidata/api/v1.0/lines/<int:line_id>/stations',
    methods=['GET']
)
def get_stations(line_id):
    rows = db.session.query(
        Station.id,
        Station.group_id,
        Station.common_name,
        Station.longitude,
        Station.latitude
    ).join(
        Line,
        Line.id == Station.line_id,
        isouter=True
    ).filter(
        Station.status == 0,
        Station.id > 1000000,
        Station.line_id == line_id,
        Line.status == 0,
        Line.category != 1
    ).order_by(
        Station.sort_code,
        Station.id
    ).all()

    if len(rows) == 0:
        abort(404)

    stations = []

    for row in rows:
        station = {
            'id': row.id,
            'group_id': row.group_id,
            'common_name': row.common_name,
            'longitude': row.longitude,
            'latitude': row.latitude
        }
        stations.append(station)

    return {'stations': stations}


@bp.route(
    '/ekidata/api/v1.0/stations/<int:station_id>/details',
    methods=['GET']
)
def get_station_details(station_id):
    row = db.session.query(
        Station.prefecture_id,
        Station.line_id,
        Station.id.label('station_id'),
        Station.group_id,
        Station.common_name.label('station_common_name'),
        Station.longitude,
        Station.latitude,
        Line.common_name.label('line_common_name')
    ).join(
        Line,
        Line.id == Station.line_id,
        isouter=True
    ).filter(
        Station.status == 0,
        Station.id == station_id,
        Station.id > 1000000
    ).order_by(
        Station.id
    ).first()

    if row is None:
        abort(404)

    details = {
        'prefecture_id': row.prefecture_id,
        'line': {
            'id': row.line_id,
            'common_name': row.line_common_name,
        },
        'station': {
            'id': row.station_id,
            'group_id': row.group_id,
            'common_name': row.station_common_name,
            'longitude': row.longitude,
            'latitude': row.latitude
        }
    }

    return details


@bp.route(
    '/ekidata/api/v1.0/station-groups/<int:station_group_id>',
    methods=['GET']
)
def get_station_groups(station_group_id):
    rows = db.session.query(
        Station.prefecture_id,
        Station.line_id,
        Station.id.label('station_id'),
        Station.common_name.label('station_name'),
        Line.common_name.label('line_name')
    ).join(
        Line,
        Line.id == Station.line_id,
        isouter=True
    ).filter(
        Station.group_id == station_group_id,
        Station.status == 0,
        Station.id > 1000000
    ).order_by(
        Station.sort_code, Station.id
    ).all()

    if len(rows) == 0:
        abort(404)

    station_groups = []

    for row in rows:
        station_group = {
            'prefecture_id': row.prefecture_id,
            'line': {
                'id': row.line_id,
                'name': row.line_name,
            },
            'station': {
                'id': row.station_id,
                'name': row.station_name
            },
        }
        station_groups.append(station_group)

    return {'station_groups': station_groups}


@bp.route(
    '/ekidata/api/v1.0/lines/<int:line_id>/connecting-stations',
    methods=['GET']
)
def get_connecting_stations(line_id):
    station_1 = aliased(Station)
    station_2 = aliased(Station)

    rows = db.session.query(
        ConnectingStation.station_id_1,
        ConnectingStation.station_id_2,
        station_1.common_name.label('common_name_1'),
        station_1.latitude.label('latitude_1'),
        station_1.longitude.label('longitude_1'),
        station_2.common_name.label('common_name_2'),
        station_2.latitude.label('latitude_2'),
        station_2.longitude.label('longitude_2')
    ).join(
        station_1,
        station_1.id == ConnectingStation.station_id_1,
        isouter=True
    ).join(
        station_2,
        station_2.id == ConnectingStation.station_id_2,
        isouter=True
    ).join(
        Line,
        Line.id == ConnectingStation.line_id,
        isouter=True
    ).filter(
        ConnectingStation.line_id == line_id,
        Line.status == 0,
        Line.category != 1
    ).order_by(
        Line.status, Line.id
    ).all()

    if len(rows) == 0:
        abort(404)

    connecting_stations = []

    for row in rows:
        connecting_station = {
            'station_1': {
                'id': row.station_id_1,
                'common_name': row.common_name_1,
                'longitude': row.longitude_1,
                'latitude': row.latitude_1,
            },
            'station_2': {
                'id': row.station_id_2,
                'common_name': row.common_name_2,
                'longitude': row.longitude_2,
                'latitude': row.latitude_2
            },
        }
        connecting_stations.append(connecting_station)

    return {'connecting_stations': connecting_stations}


@bp.route(
    (
        '/ekidata/api/v2.0'
        '/longitude/<float:longitude>'
        '/latitude/<float:latitude>'
        '/max-distance/<float:max_distance>'
        '/stations'
    ),
    methods=['GET']
)
def get_nearest_stations(longitude, latitude, max_distance):
    documents = (
        mongo.db.station
        .aggregate([
            {
                '$geoNear': {
                    'near': {'coordinates': [longitude, latitude]},
                    'distanceField': 'distance',
                    'spherical': True,
                    'distanceMultiplier': 0.001,
                    'maxDistance': max_distance * 1000,
                },
            },
            {
                '$match': {
                    'status': 0,
                },
            }
        ])
    )

    stations = []

    for document in documents:
        station = {
            'common_name': document['name']['common'],
            'lines': document['lines'],
            'location': {
                'longitude': document['location'][0],
                'latitude': document['location'][1],
            },
            'distance': document['distance'],
            'prefecture': document['prefecture'],
        }
        stations.append(station)

    if not stations:
        abort(404)

    return {'stations': stations}
