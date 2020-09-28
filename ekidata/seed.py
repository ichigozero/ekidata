import csv
import datetime

import click
from flask import Blueprint

from ekidata.models import db
from ekidata.models import Company
from ekidata.models import ConnectingStation
from ekidata.models import Line
from ekidata.models import Station
from ekidata.models import Prefecture

bp = Blueprint('seed', __name__)


@bp.cli.command()
@click.argument('csv_path')
def company(csv_path):
    clear_table_data(Company)
    print('Importing company data')

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            company = Company(
                id=row['company_cd'],
                railway_id=row['rr_cd'],
                common_name=row['company_name'],
                kana_name=row['company_name_k'],
                official_name=row['company_name_h'],
                short_name=row['company_name_r'],
                url=row['company_url'],
                category=row['company_type'],
                status=row['e_status'],
                sort_code=row['e_sort']
            )
            db.session.add(company)

        db.session.commit()

    print('Import complete')


@bp.cli.command()
@click.argument('csv_path')
def line(csv_path):
    clear_table_data(Line)
    print('Importing line data')

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            line = Line(
                id=row['line_cd'],
                company_id=row['company_cd'],
                common_name=row['line_name'],
                kana_name=row['line_name_k'],
                official_name=row['line_name_h'],
                color_code=row['line_color_c'],
                color_name=row['line_color_t'],
                category=row['line_type'],
                longitude=row['lon'],
                latitude=row['lat'],
                zoom_size=row['zoom'],
                status=row['e_status'],
                sort_code=row['e_sort']
            )
            db.session.add(line)

        db.session.commit()

    print('Import complete')


@bp.cli.command()
@click.argument('csv_path')
def station(csv_path):
    clear_table_data(Station)
    print('Importing station data')

    def _to_date(raw_date):
        if raw_date:
            if raw_date != '0000-00-00':
                return (
                    datetime
                    .datetime
                    .strptime(raw_date, '%Y-%m-%d')
                    .date()
                )

        return None

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            station = Station(
                id=row['station_cd'],
                group_id=row['station_g_cd'],
                common_name=row['station_name'],
                kana_name=row['station_name_k'],
                romaji_name=row['station_name_r'],
                line_id=row['line_cd'],
                prefecture_id=row['pref_cd'],
                post_code=row['post'],
                address=row.get('add') or row.get('address'),
                longitude=row['lon'],
                latitude=row['lat'],
                open_date=_to_date(row['open_ymd']),
                close_date=_to_date(row['close_ymd']),
                status=row['e_status'],
                sort_code=row['e_sort']
            )
            db.session.add(station)

        db.session.commit()

    print('Import complete')


@bp.cli.command()
@click.argument('csv_path')
def connecting_station(csv_path):
    clear_table_data(ConnectingStation)
    print('Importing connecting station data')

    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            connecting_station = ConnectingStation(
                line_id=row['line_cd'],
                station_id_1=row['station_cd1'],
                station_id_2=row['station_cd2']
            )
            db.session.add(connecting_station)

        db.session.commit()

    print('Import complete')


@bp.cli.command()
@click.argument('csv_path')
def prefecture(csv_path):
    clear_table_data(Prefecture)
    print('Importing prefecture data')

    with open(csv_path) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            prefecture = Prefecture(
                id=row['pref_cd'],
                name=row['pref_name']
            )
            db.session.add(prefecture)

        db.session.commit()

    print('Import complete')


def clear_table_data(model):
    print('Deleting existing data')
    db.session.query(model).delete()
    print('Delete complete')
