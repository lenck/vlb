function [ imdb ] = vggh( varargin )
%VGGH Wrapper around the vgg affine datasets
%   datasets.VggAffineDataset('Option','OptionValue',...) Constructs
%   an object which implements access to VGG Affine dataset used for
%   affine invariant detectors evaluation.
%
%   The dataset is available at: 
%   http://www.robots.ox.ac.uk/~vgg/research/affine/
%
%   This class perform automatic installation when the dataset data
%   are not available.

% Copyright (C) 2011-17 Karel Lenc, Varun Gulshan
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.rootDir = fullfile(vlb_path('datasets'), 'vggaffine');
opts.matchFramesFun = @(g) ...
  @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
  'maxOverlapError', 0.5, varargin{:});
opts = vl_argparse(opts, varargin);

% Meta about all datasets
sequences = {};
sequences{end+1} = struct('name', 'graf', 'description', 'Viewpoint angle', ...
  'labels', {{0 20 30 40 50 60}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'wall', 'description', 'Viewpoint angle', ...
  'labels', {{0 20 30 40 50 60}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'boat', 'description', 'Scale changes', ...
  'labels', {{1 1.12 1.38 1.9 2.35 2.8}}, 'imext', 'pgm');
sequences{end+1} = struct('name', 'bark', 'description', 'Scale changes', ...
  'labels', {{1 1.2 1.8 2.5 3 4}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'bikes', 'description', 'Increasing blur', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'trees', 'description', 'Increasing blur', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'ubc', 'description', 'JPEG compression', ...
  'labels',  {{0 60 80 90 95 98}}, 'imext', 'ppm');
sequences{end+1} = struct('name', 'leuven','description', 'Decreasing light', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
sequences = cell2mat(sequences);
% Root url for dataset tarballs
rootUrl = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/';
getDsetUrl = @(dset) [rootUrl, dset.name, '.tar.gz'];
getImPath = @(dset, imid) fullfile(opts.rootDir, dset.name, ...
  sprintf('img%d.%s', imid, dset.imext));

% Download the datasets
for catIdx = 1:numel(sequences)
  dset = sequences(catIdx);
  dsetDir = fileparts(getImPath(dset, 1));
  utls.provision(getDsetUrl(dset), dsetDir);
end

numImages = 6*numel(sequences);
imdb.images = cell(1, numImages);
imdb.tasks = {};

% Read the image information
imi = 1;
for catIdx = 1:numel(sequences)
  dset = sequences(catIdx);
  refim = imi;
  dsetDir = fileparts(getImPath(dset, 1));
  imSizeRef = [];
  for imi_l = 1:6
    imPath = getImPath(dset, imi_l);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi}.id = imi;
    imdb.images{imi}.name = sprintf('%s-%d', dset.name, imi_l);
    imdb.images{imi}.path = imPath;
    imdb.images{imi}.seqnum = imi_l;
    imdb.images{imi}.sequence = dset.name;
    if imi_l == 1
        imi = imi + 1;
        %Size of the first image may not be the same as other images.
        imSizeRef =  utls.get_image_size(imPath);
        continue; 
    end;
    imSize =  utls.get_image_size(imPath);
    tfs = utls.read_vgg_homography(fullfile(dsetDir, sprintf('H1to%dp', imi_l)));
    imdb.tasks{end+1} = struct('ima', imdb.images{refim}.name, ...
      'imb', imdb.images{imi}.name, ...
      'ima_id', refim, 'imb_id', imi, 'H', tfs, ...
      'ima_size', imSizeRef, 'imb_size', imSize, ...
      'sequence', dset.name, ...
      'description', struct('impair', [1, imi_l], ...
      'nuisanceName', dset.description, 'nuisanceValue', dset.labels{imi_l}));
    imi = imi + 1;
  end
end
imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'vggh';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.geometry = 'homography';
imdb.rootdir = opts.rootDir;
end

