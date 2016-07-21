function [ imdb ] = vlb_dataset_featw( varargin )

% Copyright (C) 2016 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

IMEXT = 'ppm';
SEQ_NUMIM = 6;

opts.rootDir = fullfile(vlb_root(), 'data', 'dataset-featw');
opts = vl_argparse(opts, varargin);

categories = listdir(opts.rootDir);
sequences = struct('name', {{}}, 'category', []);
for ci = 1:numel(categories)
  seq =  listdir(fullfile(opts.rootDir, categories{ci}));
  sequences.name = [sequences.name, seq];
  sequences.category = [sequences.category, ones(1, numel(seq))*ci];
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
  category = categories{sequences.category(si)};
  path = fullfile(category, sequences.name{si});
  imfiles = dir(fullfile(opts.rootDir, path, sprintf('*.%s', IMEXT)));
  assert(numel(imfiles) == SEQ_NUMIM);
  
  % TODO add check if image files do exist
  
  si_si = (si-1)*SEQ_NUMIM + 1;
  si_ei = si*SEQ_NUMIM;
  imdb.images.name(si_si:si_ei) = ...
    arrayfun(@(i) fullfile(path, sprintf('%d.%s', i, IMEXT)), ...
    1:SEQ_NUMIM, 'UniformOutput', false);
  imdb.images.category(si_si:si_ei) = sequences.category(si);
  imdb.images.sequence(si_si:si_ei) = si;
  imdb.images.num(si_si:si_ei) = 1:SEQ_NUMIM;
  imdb.images.refim_id(si_si:si_ei) = si_si;
  imdb.images.geometry{si_si} = eye(3);
  imdb.images.geometry(si_si+1:si_ei) = ...
    arrayfun(@(i) utls.read_vgg_homography(...
      fullfile(opts.rootDir, path, sprintf('H_1_%d', i))), ...
    2:SEQ_NUMIM, 'UniformOutput', false); 
end

imdb.images.geometry = cell2mat(imdb.images.geometry);
% Set up the common properties
imdb.meta.categories = categories;
imdb.meta.sequences = sequences;

% Methods
imdb.getImagePath = @(imid) fullfile(imdb.imageDir, imdb.images.name{imid});
imdb.getGsImage = @(imid) utls.imread_grayscale(imdb.getImagePath(imid));
imdb.getGeom = @(imid) imdb.images.geometry(:,:,imid);
imdb.findImageId = @(varargin) findImageId(imdb, varargin{:});
end

function imid = findImageId(imdb, category, sequence, num)
 if nargin == 1 && numel(category) == 3
   sequence = category(2); num = category(3); category = category(1);
 end
 if ischar(category)
   [found, category] = ismember(category, imdb.meta.categories);
   if ~found, error('Category %s not found.', category); end;
 end
 if ischar(sequence)
   [found, sequence] = ismember(sequence, imdb.meta.sequences.name);
   if ~found, error('Sequence %s not found.', sequence); end;
 end
 imid = imdb.images.id(...
   imdb.images.category == category &...
   imdb.images.sequence == sequence &...
   imdb.images.num == num);
end

function dirs = listdir(path)
dirs = dir(path);
is_valid = [dirs.isdir] & arrayfun(@(d) d.name(1)~='.', dirs)';
dirs = {dirs.name};
dirs = dirs(is_valid);
end
