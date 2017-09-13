# VLB: VLFeat Local Features Benchmark

A MATLAB framework for local feature evaluation.
Reimplementation of the VLBenchmarks project.
**Currenlty work in progress** so it has more than few rough edges.

## Getting Started
To setup the VLBenchmarks, run from the vlb path:
```
run ./matlab/vlb_setup.m
run ./matlab/vlb_compile.m
```
where one needs to compile the package only while running for the first time.

For example usage, see the prepared [examples](./examples/):
* [detbench.m](./example/detbench.m) - Detector benchmarks and results visualsiation
* [descbench.m](./example/descbench.m) - Descriptor benchmarks

## Basic Usage
The entry function is `vlb` which supports the following commands:

`FEATSNAME = vlb('detect', IMDBNAME, DETNAME)`  
Detects features of all images of a `IMDBNAME` image database. Features stored
`./data/features/IMDBNAME/DETNAME/` as csv files.
Additionally one can also extract the detected patches with the `extract` command.

`FEATSNAME = vlb('describe', IMDBNAME, FEATSNAME, DESCNAME)`   
Computes descriptors of all features detected by `FEATSNAME` of `IMDBNAME` image database.
Features stored in `./data/features/IMDBNAME/FEATSNAME/DESCNAME/` as csv files.

`RES = vlb('detrep', IMDBNAME, FEATSNAME)`   
`RES = vlb('dematch', IMDBNAME, FEATSNAME)`   
`RES = vlb('descmatch', IMDBNAME, FEATSNAME)`   
Evaluates the detector repeatabiliy, detector matching score or a descriptor matching score of features `FEATSNAME` in the selected dataset. Returns a table with results,
which is additionally stored in `./data/scores/BENCH/IMDBNAME/FEATSNAME` as a csv file.


## Directory structure
`matlab/+dset`   Implemented datasets (VGG-Aff, EdgeFoci, WebCam, Hsequences...).  
`matlab/+features/+det` Implemented detector wrappers.  
`matlab/+features/+desc` Implemented descriptor wrappers. Please note that some descriptors accept detected frames, some need extracted patches.

Furthermore, you can extract the features outside of this framework in order to evaluate them. Please extract e.g. `vlsift` features and follow the naming conventions.

## Running the tests
To run the tests, call:
`vlb_test`.
