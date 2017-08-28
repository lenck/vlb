function [ imdb ] = vgg( varargin )
%VLB_DATASET_VGGAFFINE Wrapper around the vgg affine datasets
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

opts.rootDir = fullfile(vlb_path(), 'data', 'dataset-vggaffine');
opts.matchFramesFun = @(g) ...
  @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
  'maxOverlapError', 0.5, varargin{:});
opts = vl_argparse(opts, varargin);

% Meta about all datasets
datasets = {};
datasets{end+1} = struct('name', 'graf', 'description', 'Viewpoint angle', ...
  'labels', {{0 20 30 40 50 60}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'wall', 'description', 'Viewpoint angle', ...
  'labels', {{0 20 30 40 50 60}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'boat', 'description', 'Scale changes', ...
  'labels', {{1 1.12 1.38 1.9 2.35 2.8}}, 'imext', 'pgm');
datasets{end+1} = struct('name', 'bark', 'description', 'Scale changes', ...
  'labels', {{1 1.2 1.8 2.5 3 4}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'bikes', 'description', 'Increasing blur', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'trees', 'description', 'Increasing blur', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'ubc', 'description', 'JPEG compression', ...
  'labels',  {{0 60 80 90 95 98}}, 'imext', 'ppm');
datasets{end+1} = struct('name', 'leuven','description', 'Decreasing light', ...
  'labels', {{1 2 3 4 5 6}}, 'imext', 'ppm');
datasets = cell2mat(datasets);
% Root url for dataset tarballs
rootUrl = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/';
getDsetUrl = @(dset) [rootUrl, dset.name, '.tar.gz'];
getImPath = @(dset, imid) fullfile(opts.rootDir, dset.name, ...
  sprintf('img%d.%s', imid, dset.imext));

% Download the datasets
for catIdx = 1:numel(datasets)
  dset = datasets(catIdx);
  dsetDir = fileparts(getImPath(dset, 1));
  if ~exist(getImPath(dset, 1), 'file')
    vl_xmkdir(dsetDir);
    fprintf('Downloading `%s` to %s.\n\tIt may take some time.\n', ...
      dset.name, dsetDir);
    untar(getDsetUrl(dset), dsetDir);
  end
end

numImages = 6*numel(datasets);
imdb.images = cell(1, numImages);
imdb.tasks = {};

% Read the image information
imi = 1;
for catIdx = 1:numel(datasets)
  dset = datasets(catIdx);
  refim = imi;
  for imi_l = 1:6
    imPath = getImPath(dset, imi_l);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi}.id = imi;
    imdb.images{imi}.name = sprintf('%s-%d', dset.name, imi_l);
    imdb.images{imi}.path = imPath;
    imdb.images{imi}.seqnum = imi_l;
    imdb.images{imi}.category = dset.name;
    if imi_l == 1, imi = imi + 1; continue; end;
    imSize =  utls.get_image_size(imPath);
    tfs = utls.read_vgg_homography(fullfile(dsetDir, sprintf('H1to%dp', imi_l)));
    imdb.tasks{end+1} = struct('ima', imdb.images{refim}.name, ...
      'imb', imdb.images{imi}.name, 'H', tfs, ...
      'ima_size', imSize, 'imb_size', imSize, ...
      'description', struct('category', dset.name, 'impair', [1, imi_l], ...
      'nuisanceName', dset.description, 'nuisanceValue', dset.labels{imi_l}));
    imi = imi + 1;
  end
end
imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'vgg';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.rootdir = opts.rootDir;
end

