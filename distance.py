#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import glob

import numpy as np
import pandas as pd
from geopy.distance import vincenty as point_distance


def ingest(fn, route_id, begin_latlng, end_latlng):
    df = pd.read_csv(fn, parse_dates=['timestamp'])
    df = df.drop(['dist_traveled', 'speed', 'trip_headsign'], axis=1)
    df = df[df.route_id == route_id]
    df['begin_distances'] = compute_distance(df, begin_latlng)
    df['end_distances'] = compute_distance(df, end_latlng)
    return df


def compute_distance(df, latlng):
    df = df.copy()
    starts = zip(df.lat, df.lon)
    return [point_distance(latlng, s).meters for s in starts]


def transit_times(df):
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

    unneeded_cols = ['begin_distances', 'end_distances', 'lat', 'lon']
    begin_mins.drop(unneeded_cols, axis=1, inplace=True)
    end_mins.drop(['vehicle_id', 'route_id'] + unneeded_cols, axis=1, inplace=True)

    result = begin_mins.join(end_mins, rsuffix='_begin', lsuffix='_end')

    duration = begin_mins.timestamp - end_mins.timestamp
    result['duration'] = duration / np.timedelta64(1, 's')

    return result


def main():
    import argparse
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('data_dir', help='Path to CSV locations')
    parser.add_argument('--route_id', help='Route ID', required=True, type=int)
    parser.add_argument('--begin_lat', help='Latitude of first stop', required=True, type=float)
    parser.add_argument('--begin_lon', help='Longitude of first stop', required=True, type=float)
    parser.add_argument('--end_lat', help='Latitude of second stop', required=True, type=float)
    parser.add_argument('--end_lon', help='Longitude of second stop', required=True, type=float)
    args = parser.parse_args()

    files = glob.glob(args.data_dir)
    for i, fname in enumerate(files):
        df = ingest(fname, args.route_id, (args.begin_lat, args.begin_lon), (args.end_lat, args.end_lon))
        times = transit_times(df)
        print(times.to_csv(header=(i == 0)))

if __name__ == '__main__':
    main()
