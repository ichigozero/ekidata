from flask import url_for


def test_get_prefectures(client, app_db):
    response = client.get(url_for('api.get_prefectures'))

    assert response.status_code == 200

    prefectures = [
        {
            'id': 13,
            'name': '東京都',
        },
        {
            'id': 14,
            'name': '神奈川県',
        },
    ]

    assert response.json['prefectures'] == prefectures


def test_get_line_api(client, app_db):
    response = client.get(url_for('api.get_lines', prefecture_id=13))

    assert response.status_code == 200

    lines = [
        {
            'id': 11302,
            'common_name': 'JR山手線',
        },
        {
            'id': 11332,
            'common_name': 'JR京浜東北線',
        },
    ]

    assert response.json['lines'] == lines


def test_get_stations_api(client, app_db):
    response = client.get(url_for('api.get_stations', line_id=11302))

    assert response.status_code == 200

    stations = [
        {
            'id': 1130220,
            'group_id': 1130220,
            'common_name': '上野',
            'longitude': 139.777043,
            'latitude': 35.71379,
        },
        {
            'id': 1130224,
            'group_id': 1130101,
            'common_name': '東京',
            'longitude': 139.766103,
            'latitude': 35.681391,
        },
        {
            'id': 1130225,
            'group_id': 1130225,
            'common_name': '有楽町',
            'longitude': 139.763806,
            'latitude': 35.675441,
        },
    ]

    assert response.json['stations'] == stations


def test_get_station_details_api(client, app_db):
    response = client.get(
        url_for('api.get_station_details', station_id=1130220)
    )

    assert response.status_code == 200

    details = {
        'prefecture_id': 13,
        'line': {
            'id': 11302,
            'common_name': 'JR山手線',
        },
        'station': {
            'id': 1130220,
            'group_id': 1130220,
            'common_name': '上野',
            'longitude': 139.777043,
            'latitude': 35.71379,
        }
    }

    assert response.json == details


def test_get_station_groups_api(client, app_db):
    response = client.get(
        url_for('api.get_station_groups', station_group_id=1130101)
    )

    assert response.status_code == 200

    station_groups = [
        {
            'prefecture_id': 13,
            'line': {
                'id': 11302,
                'name': 'JR山手線',
            },
            'station': {
                'id': 1130224,
                'name': '東京',
            },
        },
        {
            'prefecture_id': 13,
            'line': {
                'id': 11332,
                'name': 'JR京浜東北線',
            },
            'station': {
                'id': 1133222,
                'name': '東京',
            },
        },
    ]

    assert response.json['station_groups'] == station_groups


def test_get_connecting_stations_api(client, app_db):
    response = client.get(
        url_for('api.get_connecting_stations', line_id=11302)
    )

    assert response.status_code == 200

    connecting_stations = [
        {
            'station_1': {
                'id': 1130224,
                'common_name': '東京',
                'longitude': 139.766103,
                'latitude': 35.681391,
            },
            'station_2': {
                'id': 1130225,
                'common_name': '有楽町',
                'longitude': 139.763806,
                'latitude': 35.675441,
            },
        },
    ]

    assert response.json['connecting_stations'] == connecting_stations
