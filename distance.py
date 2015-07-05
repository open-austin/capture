#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import pandas as pd
import numpy as np
from geopy.distance import vincenty as point_distance


# Trip id, vehicle id, location, time
# Looking for time between location near triangle and *next* time near downtown
# for each trip id
   # Choose a reading nearest the triangle stop
   # Choose a reading nearest downtown
   # subtract the times for those two readings
   # positive is southbound


# lat lon
TRIANGLE = (30.162883, -97.790317)
REPUB_SQ = (30.266218, -97.746056)


def ingest(fn):
    df = pd.read_csv(fn, parse_dates=['timestamp'])
    df = df.drop(['dist_traveled', 'speed', 'trip_headsign'], axis=1)
    df = df[df.route_id == 801]
    df['triangle_distances'] = compute_distance(df, TRIANGLE)
    df['repub_distances'] = compute_distance(df, REPUB_SQ)
    return df


def nearest_readings(df):
    return df.groupby('trip_id').idxmin()


def compute_distance(df, target):
    df = df.copy()
    starts = zip(df.lat, df.lon)
    return [point_distance(target, s).meters for s in starts]


def transit_times(df):
    mins = nearest_readings(df)
    triangle_mins = df.loc[mins.triangle_distances].set_index('trip_id')
    repub_mins = df.loc[mins.repub_distances].set_index('trip_id')

    unneeded_cols = [
        'triangle_distances',
        'repub_distances',
        'lat',
        'lon',
    ]

    triangle_mins.drop(unneeded_cols, axis=1, inplace=True)
    repub_mins.drop(
        ['vehicle_id', 'route_id'] + unneeded_cols,
        axis=1, inplace=True)
    result = triangle_mins.join(repub_mins, rsuffix='_tri', lsuffix='_repub')
    duration = triangle_mins.timestamp - repub_mins.timestamp
    result['duration'] = duration / np.timedelta64(1, 's')
    return result


def main():
    """Run main."""
    import argparse
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('day_file', help='CSV containing day data')
    args = parser.parse_args()
    df = ingest(args.day_file)
    times = transit_times(df)
    print(times.to_csv())
    return 0

if __name__ == '__main__':
    main()
