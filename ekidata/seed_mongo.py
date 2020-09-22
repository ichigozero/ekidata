import datetime

import click
import pandas as pd
from flask import Blueprint
from pymongo import GEOSPHERE

from ekidata import mongo

bp = Blueprint('seed-mongo', __name__)


@bp.cli.command()
@click.argument('station_csv_path')
@click.argument('line_csv_path')
@click.argument('prefecture_csv_path')
def station(
        station_csv_path,
        line_csv_path,
        prefecture_csv_path
):
    print('Deleting existing data')
    result = mongo.db.station.delete_many({})
    print(
        '{} collections of "station" document have been deleted'
        .format(result.deleted_count)
    )

    print('Processing raw station data')

    df_station = pd.read_csv(station_csv_path)

    old_row_count = len(df_station.index)
    df_station.drop(
        ['station_cd', 'station_g_cd', 'e_sort'],
        axis=1,
        inplace=True
    )
    df_station.drop_duplicates(
        subset=['lon', 'lat', 'station_name', 'line_cd'],
        keep='first',
        inplace=True
    )
    df_station.reset_index(drop=True, inplace=True)
    new_row_count = len(df_station.index)

    df_line = pd.read_csv(line_csv_path)
    df_prefecture = pd.read_csv(prefecture_csv_path)

    print(
        '{} duplicated rows have been deleted'
        .format(old_row_count - new_row_count)
    )
    print('Importing station data to DB')

    mongo.db.station.create_index([('location', GEOSPHERE)])

    def _to_date(raw_date):
        if raw_date:
            if raw_date != '0000-00-00':
                return (
                    datetime
                    .datetime
                    .strptime(raw_date, '%Y-%m-%d')
                )

        return None

    for index, row in df_station.iterrows():
        prefecture_name = (
            df_prefecture
            .loc[df_prefecture['pref_cd'] == row['pref_cd'], 'pref_name']
            .iloc[0]
        )
        line_name = (
            df_line
            .loc[df_line['line_cd'] == row['line_cd'], 'line_name']
            .iloc[0]
        )

        station = {
            'name': {
              'common': row['station_name'],
              'kana': row['station_name_k'],
              'romaji': row['station_name_r'],
            },
            'prefecture': prefecture_name,
            'post_code': row['post'],
            'address': row.get('add') or row.get('address'),
            'location': [row['lon'], row['lat']],
            'open_date': _to_date(row['open_ymd']),
            'close_date': _to_date(row['close_ymd']),
            'status': row['e_status'],
        }
        mongo.db.station.update_one(
            {
                'location': [row['lon'], row['lat']],
                'name.common': row['station_name'],
            },
            {
                '$setOnInsert': station,
                '$push': {'lines': line_name}
            },
            upsert=True
        )
        print(
            '\r{} of {} rows have been imported'
            .format((index + 1), new_row_count),
            end=''
        )
    print('\nImport complete')
