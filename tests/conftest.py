import datetime

import pytest

from config import Config
from ekidata import create_app
from ekidata import db
from ekidata.models import ConnectingStation
from ekidata.models import Line
from ekidata.models import Station


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


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
