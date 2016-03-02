# capture

A repo to answer questions about public transit in Austin. CapMetro vehicle location data is collected by [scascketta/CapMetrics](https://github.com/scascketta/CapMetrics].

To start, this project will try to answer:

- Is the 801 faster than the 1? If so, where?

https://github.com/open-austin/project-ideas/issues/3

### Installation

1. Clone the capture repository https://github.com/open-austin/capture
2. Clone the CapMetrics repository https://github.com/scascketta/CapMetrics
3. Install the requirements via `pip install -r requirements.txt`
4. Run one of the examples in the Usage section.

### Usage

`$CAPMETRICS_PATH` is the path to the CapMetrics repository.

`distance.py` transforms a day of vehicle locations into trips with travel time, given a route id and the coordinates for two stops along the route.

To get the travel times for the 801 between Triangle Station and Republic Square Park Station on June 3, 2015:

```sh
python distance.py --route_id 801 --name triangle-to-republic --begin_lat 30.162883 --begin_lon -97.790317 --end_lat 30.266218 --end_lon -97.746056  --glob "2015-06-03" --capmetrics_path ../CapMetrics
```

To get the travel times for the 801 between Tech Ridge Bay I and Southpark Meadows Station for **all days in 2016**:

```sh
python distance.py --route_id 801 --name techridge-to-southpark --begin_lat 30.418199 --begin_lon -97.668243 --end_lat 30.162883 --end_lon -97.790317  --glob "2016*" --capmetrics_path ../CapMetrics
```

To get the travel times for the 1 between Tech Ridge Bay D and Bluff Springs/William Cannon for **all days in 2016**:

```sh
python distance.py --route_id 1 --name techridge-to-cannon --begin_lat 30.418534 --begin_lon -97.668904 --end_lat 30.189427 --end_lon -97.767879  --glob "2016*" --capmetrics_path ../CapMetrics
```

#####  Data for the visualizations:

###### 801 vs 1

```sh
# end to end
python distance.py --route_id 1 --name techridge-to-cannon --begin_lat 30.418534 --begin_lon -97.668904 --end_lat 30.189427 --end_lon -97.767879  --glob "2016*" --capmetrics_path ../CapMetrics
python distance.py --route_id 801 --name techridge-to-southpark --begin_lat 30.418199 --begin_lon -97.668243 --end_lat 30.162883 --end_lon -97.790317  --glob "2016*" --capmetrics_path ../CapMetrics
# triangle to republic square
python distance.py --route_id 801 --begin_lat 30.162883 --begin_lon -97.790317 --end_lat 30.266218 --end_lon -97.746056 --name triangle-to-republic --glob "2016*" --capmetrics_path ../CapMetrics
python distance.py --route_id 1 --begin_lat 30.162883 --begin_lon -97.790317 --end_lat 30.266218 --end_lon -97.746056 --name triangle-to-republic --glob "2016*" --capmetrics_path ../CapMetrics
```

###### 803 vs 3

```sh
...
```

### Installation

1. git clone git@github.com:scascketta/CapMetrics.git
2. git clone git@github.com:open-austin/capture.git
3. cd capture
4. pip install -r requirements.txt
