#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import argparse
import glob
import os

import numpy as np
import pandas as pd
from geopy.distance import vincenty as point_distance


def ingest(fn, route_id, begin_latlng, end_latlng):
    df = pd.read_csv(fn, parse_dates=['timestamp'])
    df = df.drop(['speed', 'trip_headsign'], axis=1)
    df = df[df.route_id == route_id]
    df['begin_distances'] = compute_distance(df, begin_latlng)
    df['end_distances'] = compute_distance(df, end_latlng)
    return df


def compute_distance(df, latlng):
    df = df.copy()
    starts = zip(df.latitude, df.longitude)
    return [point_distance(latlng, s).meters for s in starts]


def parse_duration(df):
    '''
    for each trip id
        choose a reading nearest the begin stop
        choose a reading nearest downtown
        subtract the times for those two readings
        positive is southbound
    '''

    mins = df.groupby('trip_id').idxmin()
    begin_mins = df.loc[mins.begin_distances].set_index('trip_id')
    end_mins = df.loc[mins.end_distances].set_index('trip_id')

    unneeded_cols = ['begin_distances', 'end_distances', 'latitude', 'longitude']
    begin_mins.drop(unneeded_cols, axis=1, inplace=True)
    end_mins.drop(['vehicle_id', 'route_id'] + unneeded_cols, axis=1, inplace=True)

    result = begin_mins.join(end_mins, rsuffix='_begin', lsuffix='_end')

    duration = begin_mins.timestamp - end_mins.timestamp
    result['duration'] = duration / np.timedelta64(1, 's')

    return result


def parse_duration_by_hour(df):
    df['duration_abs'] = df['duration'].abs()
    df['hour'] = df['timestamp_begin'].apply(
        lambda x: x.tz_localize('UTC').tz_convert('US/Central').hour
    )
    df_byhour = df.groupby('hour')

    results = pd.concat([
        df_byhour['duration_abs'].count(),
        df_byhour['duration_abs'].mean()
    ], axis=1, keys=['count', 'mean'])

    return results.reindex(index=range(0, 24))


def parse(capmetrics_path=None, leglob=None, route_id=None, begin_lat=None, begin_lon=None, end_lat=None, end_lon=None, name=None):
    df_total = pd.DataFrame()

    data_glob = os.path.join(capmetrics_path, 'data', 'vehicle_positions', leglob)
    files = glob.glob(data_glob)
    for i, fname in enumerate(files):
        print('({}/{}) Ingesting {}'.format(i + 1, len(files), fname))
        try:
            df_ingested = ingest(fname, route_id, (begin_lat, begin_lon), (end_lat, end_lon))
            df_duration = parse_duration(df_ingested)
            df_total = pd.concat([df_total, df_duration])
        except Exception as e:
            print(e)
            print('Skipping ', fname)

    if df_total.empty:
        print('No vehicle positions found')
        return

    return parse_duration_by_hour(df_duration)


def main():
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--capmetrics_path', help='Path to the capmetrics directory', required=True, type=str)
    parser.add_argument('--glob', help='Glob of vehicle positions CSV files', required=True, type=str)
    parser.add_argument('--name', help='Name of the output file', required=True, type=str)
    parser.add_argument('--route_id', help='Route ID', required=True, type=int)
    parser.add_argument('--begin_lat', help='Latitude of first stop', required=True, type=float)
    parser.add_argument('--begin_lon', help='Longitude of first stop', required=True, type=float)
    parser.add_argument('--end_lat', help='Latitude of second stop', required=True, type=float)
    parser.add_argument('--end_lon', help='Longitude of second stop', required=True, type=float)
    args = parser.parse_args()

    results = parse(
        capmetrics_path=args.capmetrics_path,
        name=args.name,
        leglob=args.glob,
        route_id=args.route_id,
        begin_lat=args.begin_lat,
        begin_lon=args.begin_lon,
        end_lat=args.end_lat,
        end_lon=args.end_lon
    )

    output_filename = '{route_id}_{name}_{glob}'.format(route_id=args.route_id, glob=args.glob, name=args.name)
    output_path_duration_by_hour = 'results/duration_by_hour/{}.csv'.format(output_filename)
    results.to_csv(output_path_duration_by_hour, header=True, sep='\t')
    print('Saved duration by hour to {}'.format(output_path_duration_by_hour))

if __name__ == '__main__':
    main()
