from flask import url_for

stations = [
    {
        'common_name': '麻布十番',
        'lines': ['東京メトロ南北線', '都営大江戸線'],
        'location': {
            'longitude': 139.737051,
            'latitude': 35.654682,
        },
        'distance': 0.2690797802047325,
        'prefecture': '東京部',
    },
    {
        'common_name': '赤羽橋',
        'lines': ['都営大江戸線'],
        'location': {
            'longitude': 139.743642,
            'latitude': 35.655007,
        },
        'distance': 0.3294241454061509,
        'prefecture': '東京部',
    },
    {
        'common_name': '神谷町',
        'lines': ['東京メトロ日比谷線'],
        'location': {
            'longitude': 139.745069,
            'latitude': 35.662978,
        },
        'distance': 0.9994615000109301,
        'prefecture': '東京部',
    },
]


def test_get_stations_within_half_kilometers(client, app_mongodb):
    response = client.get(url_for(
        'routes.get_nearest_stations',
        longitude=139.74,
        latitude=35.655,
        max_distance=0.5
    ))

    assert response.status_code == 200
    assert response.json['stations'] == stations[:2]


def test_get_stations_within_one_kilometer(client, app_mongodb):
    response = client.get(url_for(
        'routes.get_nearest_stations',
        longitude=139.74,
        latitude=35.655,
        max_distance=1.0
    ))

    assert response.status_code == 200
    assert response.json['stations'] == stations
