from flask import abort

from ekidata import mongo
from ekidata.api import bp


@bp.route(
    (
        '/v2.0'
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
