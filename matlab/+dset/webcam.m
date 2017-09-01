function [ imdb ] = webcam( varargin )

% Copyright (C) 2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

NUMIM = 10;
DATADIR = 'WebcamRelease';
NUMSEQUENCES = 6;

opts.url = 'https://documents.epfl.ch/groups/c/cv/cvlab-unit/www/data/keypoints/WebcamRelease.tar.gz';
opts.rootDir = fullfile(vlb_path(), 'data', 'dataset-webcam');
opts.matchFramesFun = @(g) ...
  @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
  'maxOverlapError', 0.5, varargin{:});
opts.impath = 'image_color';
opts = vl_argparse(opts, varargin);

utls.provision(opts.url, opts.rootDir);

dataDir = fullfile(opts.rootDir, DATADIR);
getImPath = @(seq, imname) fullfile(dataDir, seq, 'test', opts.impath, imname);
sequences = sort(utls.listdirs(dataDir));
assert(numel(sequences) == NUMSEQUENCES, ...
  'Invalid number of sequences found.');

imdb.images = {};
imdb.tasks = {};
rfile = @(path) strtrim(strsplit(strtrim(fileread(path)), '\n'));

imi = 1;
for sIdx = 1:numel(sequences)
  sequence = sequences{sIdx};
  testimgs = rfile(fullfile(dataDir, sequence, 'test', 'test_imgs.txt'));
  valimgs = rfile(fullfile(dataDir, sequence, 'test', 'validation_imgs.txt'));
  allimgs = [valimgs, testimgs];
  allimgs_istest = [false(1, numel(valimgs)), true(1, numel(valimgs))];
  for imi_l = 1:numel(allimgs)
    [~, filename, ext] = fileparts(allimgs{imi_l});
    imPath = getImPath(sequence, [filename, ext]);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi}.id = imi;
    imdb.images{imi}.name = sprintf('%s-%d', sequence, filename);
    imdb.images{imi}.path = imPath;
    imdb.images{imi}.sequence = sequence;
    imdb.images{imi}.istest = allimgs_istest(imi_l);
    imdb.images{imi}.isval = ~allimgs_istest(imi_l);
    imdb.images{imi}.imsize =  utls.get_image_size(imPath);
    imi = imi + 1;
  end
  pairs = [1:NUMIM; (1:NUMIM) + NUMIM];
  pairs = [pairs, pairs + 2*NUMIM];
  for pi = 1:size(pairs, 2)
    pair = pairs(:, pi);
    imdb.tasks{end+1} = struct('ima', imdb.images{pair(1)}.name, ...
      'imb', imdb.images{pair(2)}.name, 'H', eye(3), ...
      'ima_size', imdb.images{pair(1)}.imsize, ...
      'imb_size', imdb.images{pair(2)}.imsize, ...
      'description', struct('sequence', sequence, ...
      'impair', pair'));
  end
end

imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'webcam';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.geometry = 'homography';
imdb.rootdir = opts.rootDir;

end


