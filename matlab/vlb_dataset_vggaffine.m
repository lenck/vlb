function [ imdb ] = vlb_dataset_vggaffine( category, varargin )
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
%
%   Following options are supported:
%
%   Category :: ['graf']
%     The category within the VGG dataset, has to be one of
%     'bikes', 'trees', 'graf', 'wall', 'bark', 'boat', 'leuven', 'ubc'

% Copyright (C) 2011-16 Karel Lenc, Varun Gulshan
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.rootDir = fullfile(vlb_root(), 'data', 'dataset_vggaffine');
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

[catFound, catIdx] = ismember(category, {datasets.name});
assert(catFound, 'Invalid category');

dset = datasets(catIdx);
dsetDir = fileparts(getImPath(dset, 1));
if ~exist(getImPath(dset, 1), 'file')
  vl_xmkdir(dsetDir);
  fprintf('Downloading `%s` to %s.\n', dset.name, dsetDir);
  untar(getDsetUrl(dset), dsetDir);
end

imdb.imageDir = dsetDir;
imdb.images.id = 1:6;
imdb.images.name = cell(1, 6);
imdb.images.geometry = cell(1, 6);
imdb.images.label = dset.labels;

% Read the image information
for imi = 1:6
  imPath = getImPath(dset, imi);
  assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
  [~, imName, imExt] = fileparts(imPath);
  imdb.images.name{imi} = [imName, imExt];
  imSize =  utls.get_image_size(imPath);
  tfs = eye(3);
  if imi > 1
    [tfs(:,1), tfs(:,2), tfs(:,3)] = textread( ...
      fullfile(dsetDir, sprintf('H1to%dp', imi)), '%f %f %f%*[^\n]');
  end
  imdb.images.geometry{imi} = struct('H', tfs, 'imsize', imSize, ...
    'refimsize', imSize);
end
imdb.images.geometry = cell2mat(imdb.images.geometry);
% Set up the common properties
imdb.meta.category = category;
imdb.meta.description = dset.description;

imdb.getGsImage = @(imid) ...
  utls.imread_grayscale(fullfile(imdb.imageDir, imdb.images.name{imid}));
imdb.getGeom = @(imid) imdb.images.geometry(imid);
end

