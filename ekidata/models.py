from ekidata import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    railway_id = db.Column(
        db.SmallInteger,
        nullable=False,
        index=True
    )
    common_name = db.Column(db.String(256), nullable=False)
    kana_name = db.Column(db.String(256))
    official_name = db.Column(db.String(256))
    short_name = db.Column(db.String(256))
    url = db.Column(db.String(512))
    category = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger)
    sort_code = db.Column(db.SmallInteger)
    lines = db.relationship('Line', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company {}>'.format(self.common_name)


class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey('company.id'),
        nullable=False,
        index=True
    )
    common_name = db.Column(db.String(256), nullable=False)
    kana_name = db.Column(db.String(256))
    official_name = db.Column(db.String(256))
    color_code = db.Column(db.String(8))
    color_name = db.Column(db.String(32))
    category = db.Column(db.SmallInteger)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    zoom_size = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger)
    sort_code = db.Column(db.Integer)
    stations = db.relationship('Station', backref='line', lazy='dynamic')
    connecting_stations = db.relationship(
        'ConnectingStation',
        backref='line',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Line {}>'.format(self.common_name)


class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    group_id = db.Column(db.Integer, nullable=False, index=True)
    common_name = db.Column(db.String(256), nullable=False)
    kana_name = db.Column(db.String(256))
    romaji_name = db.Column(db.String(256))
    line_id = db.Column(
        db.Integer,
        db.ForeignKey('line.id'),
        nullable=False,
        index=True
    )
    prefecture_id = db.Column(
        db.SmallInteger,
        db.ForeignKey('prefecture.id'),
        index=True
    )
    post_code = db.Column(db.String(32))
    address = db.Column(db.String(1024))
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    open_date = db.Column(db.DateTime)
    close_date = db.Column(db.DateTime)
    status = db.Column(db.SmallInteger)
    sort_code = db.Column(db.Integer)

    def __repr__(self):
        return '<Station {}>'.format(self.common_name)


class ConnectingStation(db.Model):
    line_id = db.Column(
        db.Integer,
        db.ForeignKey('line.id'),
        primary_key=True,
        autoincrement=False
    )
    station_id_1 = db.Column(
        db.Integer,
        db.ForeignKey('station.id'),
        primary_key=True,
        autoincrement=False
    )
    station_id_2 = db.Column(
        db.Integer,
        db.ForeignKey('station.id'),
        primary_key=True,
        autoincrement=False
    )
    stations_1 = db.relationship(
        'Station',
        backref='station_1',
        foreign_keys=[station_id_1]
    )
    stations_2 = db.relationship(
        'Station',
        backref='station_2',
        foreign_keys=[station_id_2]
    )


class Prefecture(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    stations = db.relationship(
        'Station',
        backref='prefecture',
        lazy='dynamic'
    )

    def __repr__(self):
        return '<Prefecture {}>'.format(self.name)
