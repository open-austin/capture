# capture

A repo to answer questions about public transit in Austin. CapMetro vehicle location data is collected by [scascketta/CapMetrics](https://github.com/scascketta/CapMetrics].

To start, this project will try to answer:

- Is the 801 faster than the 1? If so, where?

### Usage

`distance.py` transforms a day of vehicle locations into trips with travel time, given a route id and the coordinates for two stops along the route.

```sh
python distance.py \
    --route 801 \
    --begin_lat 30.162883 \
    --begin_lon -97.790317 \
    --end_lat 30.266218 \
    --end_lon -97.746056 \
    ../CapMetrics/data/vehicle_positions/2015-07-03.csv
```

### Installation

1. git clone git@github.com:scascketta/CapMetrics.git
2. git clone git@github.com:open-austin/capture.git
3. cd capture
4. pip install -r requirements.txt
