# VLB: VLFeat Local Features Benchmark

A framework for local feature evaluation.
Reimplementation of the VLBenchmarks project.
**Currenlty work in progress** so it has more than few rough edges.

MATLAB implementation: [Karel Lenc](https://github.com/lenck)   
Python implementation: [Xu Zhang](https://github.com/spongezhang)

## Getting Started with MATLAB implementation
Setup matlab mex environment, before starting to setup vlb.

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

## Custom Features
For custom features, you can either add your own wrapper to `matlab/+features/+det` or `matlab/+features/+desc`, depending whether the input is an image or patches/detected keypoints. Afterwards, you can use the vlb interface directly.

However, you can also compute the features outside of MATLAB and store them as CSV files. To get the list of image paths and target feature paths in format: `IMAGEPATH;TARGET_FRAMESPATH;TARGET_DESCSPATH` you can run:
```
vlb imagelist IMDBNAME FEATSNAME
```
Typically, this would create a file in `data/IMDBNAME-FEATSNAME.csv`

The format of the CSV files is one descriptor/frame per line. The frames or **one-indexed** (center of the first image pixel has a coordinate [1, 1]) and in format of `vl_plotframe` (`[c, r]` for a point, `[c, r, s]` for a disc, `[c, r, s, rot]` for oriented disc, `[c, r, S11, S12, S22]` for ellipse, `[c, r, A11, A12, A21, A22]` for oriented ellipse/affine frame).

## Directory structure
`data/features/DATASET/FEATURES` Compputed local features in csv format (see `vlb detect` and `vlb describe`)
`data/patches/DATASET/FEATURES` Extracted patches as png images (see `vlb extract`)
`data/scores/BENCHMARK/DATASET/FEATURES` Computed benchmark scores, stored as .csv tables
`datasets` Downloaded datasets
`matlab` MATLAB source code
`matlab/+dset`   Implemented datasets (VGG-Aff, EdgeFoci, WebCam, Hsequences...).  
`matlab/+features/+det` Implemented detector wrappers.  
`matlab/+features/+desc` Implemented descriptor wrappers. Please note that some descriptors accept detected frames, some need extracted patches.

Furthermore, you can extract the features outside of this framework in order to evaluate them. Please extract e.g. `vlsift` features and follow the naming conventions.

## Compile Conflicts
`mex` command may be recognized as `mex` command in texlive. Make sure that the matlab/bin path is added to system PATH before the directory of mex in texlive.

## Running the tests
To run the tests, call:
`vlb_test`.
