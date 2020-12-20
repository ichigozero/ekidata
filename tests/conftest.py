import datetime

import pytest
from pymongo import GEOSPHERE

from config import Config
from ekidata import create_app
from ekidata import db
from ekidata import mongo
from ekidata.models import ConnectingStation
from ekidata.models import Line
from ekidata.models import Prefecture
from ekidata.models import Station


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    MONGO_URI = 'mongodb://localhost:27017/ekidata-test'


@pytest.fixture(scope='module')
def app():
    app = create_app(TestConfig)

    with app.app_context():
        app.test_request_context().push()
        yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def app_db(app):
    db.create_all()

    prefecture_tokyo = Prefecture(
        id=13,
        name='東京都',
    )
    prefecture_kanagawa = Prefecture(
        id=14,
        name='神奈川県',
    )
    line_keihin_tohoku = Line(
        id=11332,
        company_id=2,
        common_name='JR京浜東北線',
        kana_name='ケイヒントウホクセン',
        official_name='JR京浜東北線',
        color_code='',
        color_name='',
        category='',
        longitude=139.6425120970631,
        latitude=35.63929555924292,
        zoom_size=10,
        status=0,
        sort_code=11332,
    )
    line_yamanote = Line(
        id=11302,
        company_id=2,
        common_name='JR山手線',
        kana_name='ヤマノテセン',
        official_name='JR山手線',
        color_code='',
        color_name='',
        category='',
        longitude=139.73522275686264,
        latitude=35.69302730762992,
        zoom_size=12,
        status=0,
        sort_code=11302,
    )
    station_ueno = Station(
        id=1130220,
        group_id=1130220,
        common_name='上野',
        kana_name='',
        romaji_name='',
        line_id=11302,
        prefecture_id=13,
        post_code='110-0005',
        address='東京都台東区上野七丁目1-1',
        longitude=139.777043,
        latitude=35.71379,
        open_date=datetime.date(1883, 7, 28),
        close_date=None,
        status=0,
        sort_code=1130220,
    )
    station_tokyo_1 = Station(
        id=1130224,
        group_id=1130101,
        common_name='東京',
        kana_name='',
        romaji_name='',
        line_id=11302,
        prefecture_id=13,
        post_code='100-0005',
        address='東京都千代田区丸の内一丁目9-1',
        longitude=139.766103,
        latitude=35.681391,
        open_date=datetime.date(1914, 12, 20),
        close_date=None,
        status=0,
        sort_code=1130224,
    )
    station_tokyo_2 = Station(
        id=1133222,
        group_id=1130101,
        common_name='東京',
        kana_name='',
        romaji_name='',
        line_id=11332,
        prefecture_id=13,
        post_code='100-0005',
        address='東京都千代田区丸の内一丁目',
        longitude=139.766103,
        latitude=35.681391,
        open_date=None,
        close_date=None,
        status=0,
        sort_code=1131201,
    )
    station_yurakucho = Station(
        id=1130225,
        group_id=1130225,
        common_name='有楽町',
        kana_name='',
        romaji_name='',
        line_id=11302,
        prefecture_id=13,
        post_code='100-0006',
        address='東京都千代田区有楽町二丁目9',
        longitude=139.763806,
        latitude=35.675441,
        open_date=datetime.date(1910, 6, 25),
        close_date=None,
        status=0,
        sort_code=1130225,
    )
    connecting_station = ConnectingStation(
        line_id=11302,
        station_id_1=1130224,
        station_id_2=1130225,
    )

    db.session.add_all([
        prefecture_tokyo,
        prefecture_kanagawa,
        station_tokyo_1,
        station_tokyo_2,
        station_ueno,
        station_yurakucho,
        connecting_station,
        line_keihin_tohoku,
        line_yamanote,
    ])
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope='module')
def app_mongodb(app):
    stations = [
        {
            'name': {
              'common': '麻布十番',
              'kana': '',
              'romaji': '',
            },
            'prefecture': '東京部',
            'post_code': '106-0045',
            'address': '港区麻布十番４-４-９',
            'location': [139.737051, 35.654682],
            'lines': ['東京メトロ南北線', '都営大江戸線'],
            'open_date': None,
            'close_date': None,
            'status': 0,
        },
        {
            'name': {
              'common': '赤羽橋',
              'kana': '',
              'romaji': '',
            },
            'prefecture': '東京部',
            'post_code': '106-0044',
            'address': '港区東麻布１-２８-１３',
            'location': [139.743642, 35.655007],
            'lines': ['都営大江戸線'],
            'open_date': None,
            'close_date': None,
            'status': 0,
        },
        {
            'name': {
              'common': '神谷町',
              'kana': '',
              'romaji': '',
            },
            'prefecture': '東京部',
            'post_code': '105-0001',
            'address': '港区虎ノ門５-１２-１１',
            'location': [139.745069, 35.662978],
            'lines': ['東京メトロ日比谷線'],
            'open_date': None,
            'close_date': None,
            'status': 0,
        },
    ]

    mongo.db.station.create_index([('location', GEOSPHERE)])
    mongo.db.station.insert_many(stations)

    yield mongo

    mongo.db.command('dropDatabase')
