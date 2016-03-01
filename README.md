# capture

A repo to answer questions about public transit in Austin. CapMetro vehicle location data is collected by [scascketta/CapMetrics](https://github.com/scascketta/CapMetrics].

To start, this project will try to answer:

- Is the 801 faster than the 1? If so, where?

https://github.com/open-austin/project-ideas/issues/3

### Usage

`distance.py` transforms a day of vehicle locations into trips with travel time, given a route id and the coordinates for two stops along the route.

To get the travel times for the 801 between Triangle Station and Republic Square Park Station on June 3, 2015:

```sh
python distance.py \
    --route_id 801 \
    --begin_lat 30.162883 \
    --begin_lon -97.790317 \
    --end_lat 30.266218 \
    --end_lon -97.746056 \
    $CAPMETRICS_PATH/data/vehicle_positions/2015-07-03.csv > data/2015-07-03-801_triangle_republic.csv
```

To get the travel times for the 801 between Tech Ridge Bay I and Southpark Meadows Station for **all days**:

```sh
python distance.py \
    --route_id 801 \
    --begin_lat 30.418199 \
    --begin_lon -97.668243 \
    --end_lat 30.162883 \
    --end_lon -97.790317 \
    "$CAPMETRICS_PATH/data/vehicle_positions/*.csv" > data/801_techridge_southpark.csv
```

To get the travel times for the 1 between Tech Ridge Bay D and Bluff Springs/William Cannon for **all days**:

```sh
python distance.py \
    --route_id 1 \
    --begin_lat 30.418534 \
    --begin_lon -97.668904 \
    --end_lat 30.189427 \
    --end_lon -97.767879 \
    "$CAPMETRICS_PATH/data/vehicle_positions/*.csv" > data/1_techridge_bluff.csv
```

```
python distance.py \
    --route_id 1 \
    --begin_lat 30.162883 \
    --begin_lon -97.790317 \
    --end_lat 30.266218 \
    --end_lon -97.746056 \
    "$CAPMETRICS_PATH/data/vehicle_positions/*.csv" > data/1_triangle_republic.csv
python distance.py \
    --route_id 801 \
    --begin_lat 30.162883 \
    --begin_lon -97.790317 \
    --end_lat 30.266218 \
    --end_lon -97.746056 \
    "$CAPMETRICS_PATH/data/vehicle_positions/*.csv" > data/801_triangle_republic.csv
```

### Installation

1. git clone git@github.com:scascketta/CapMetrics.git
2. git clone git@github.com:open-austin/capture.git
3. cd capture
4. pip install -r requirements.txt
