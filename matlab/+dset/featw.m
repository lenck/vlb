function [ imdb ] = vlb_dataset_featw( varargin )

% Copyright (C) 2016 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

IMEXT = 'ppm';
SEQ_NUMIM = 6;

opts.rootDir = fullfile(vlb_path(), 'data', 'dataset-featw', 'dataset_release');
opts = vl_argparse(opts, varargin);

categories = {'illum', 'viewpoint'};
sequences.name = utls.listdirs(opts.rootDir);
sequences.category_id  = zeros(1, numel(sequences.name));
for si = 1:numel(sequences.name)
  if strcmp(sequences.name{si}(1:2), 'i_')
    sequences.category_id(si) = 1;
  elseif strcmp(sequences.name{si}(1:2), 'v_')
    sequences.category_id(si) = 2;
  else
    error('Invalid category');
  end
end

numImages = numel(sequences.name) * SEQ_NUMIM;
imdb.imageDir = opts.rootDir;
imdb.images.id = 1:numImages;
imdb.images.name = cell(1, numImages);
imdb.images.category = zeros(1, numImages);
imdb.images.sequence = zeros(1, numImages);
imdb.images.num = zeros(1, numImages);
imdb.images.refim_id = [];
imdb.images.geometry = cell(1, 1, numImages);

for si = 1:numel(sequences.name)
  path = fullfile(sequences.name{si});
  imfiles = dir(fullfile(opts.rootDir, path, sprintf('*.%s', IMEXT)));
  assert(numel(imfiles) == SEQ_NUMIM);
  
  % TODO add check if image files do exist
  
  si_si = (si-1)*SEQ_NUMIM + 1;
  si_ei = si*SEQ_NUMIM;
  imdb.images.name(si_si:si_ei) = ...
    arrayfun(@(i) fullfile(path, sprintf('%d.%s', i, IMEXT)), ...
    1:SEQ_NUMIM, 'UniformOutput', false);
  imdb.images.category(si_si:si_ei) = sequences.category_id(si);
  imdb.images.sequence(si_si:si_ei) = si;
  imdb.images.num(si_si:si_ei) = 1:SEQ_NUMIM;
  imdb.images.refim_id(si_si:si_ei) = si_si;
  
  imdb.images.geometry{si_si}.H = eye(3);
  imdb.images.geometry{si_si}.imsize = ...
    utls.get_image_size(fullfile(imdb.imageDir, imdb.images.name{si_si}));
  imdb.images.geometry{si_si}.refimsize = imdb.images.geometry{si_si}.imsize;
  
  for imi = 2:SEQ_NUMIM
    imdb.images.geometry{si_si+imi-1}.H = utls.read_vgg_homography(...
        fullfile(opts.rootDir, path, sprintf('H_1_%d', imi)));
    imdb.images.geometry{si_si+imi-1}.imsize = ...
      utls.get_image_size(fullfile(imdb.imageDir, imdb.images.name{si_si+imi-1}));
    imdb.images.geometry{si_si+imi-1}.refimsize = imdb.images.geometry{si_si}.imsize;
  end
end

imdb.images.geometry = cell2mat(imdb.images.geometry);
% Set up the common properties
imdb.meta.categories = categories;
imdb.meta.sequences = sequences;

% Methods
imdb.getImagePath = @(imid) fullfile(imdb.imageDir, imdb.images.name{imid});
imdb.getGsImage = @(imid) utls.imread_grayscale(imdb.getImagePath(imid));
imdb.getGeom = @(varargin) getGeom(imdb, varargin{:});
imdb.findImageId = @(varargin) findImageId(imdb, varargin{:});
end

function geom = getGeom(imdb, ia, ib)
geom_ref2a = imdb.images.geometry(:,:,ia);
if nargin < 3, geom = geom_ref2a; return; end
% Compose the homographies
geom_ref2b = imdb.images.geometry(:,:,ib);
geom = struct('H', geom_ref2b.H / geom_ref2a.H, ...
  'refimsize', geom_ref2a.imsize, 'imsize', geom_ref2b.imsize);
end

function imid = findImageId(imdb, sequence, num)
 if nargin == 1 && numel(sequence) == 2
   num = sequence(2); sequence = sequence(1);
 end
 if ischar(sequence)
   [found, sequence] = ismember(sequence, imdb.meta.sequences.name);
   if ~found, error('Sequence %s not found.', sequence); end;
 end
 imid = imdb.images.id(imdb.images.sequence == sequence &...
   imdb.images.num == num);
end
