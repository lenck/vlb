function [ imdb ] = webcam( varargin )

% Copyright (C) 2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

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

imi = 1; lastim = 0;
for sIdx = 1:numel(sequences)
  sequence = sequences{sIdx};
  testimgs = rfile(fullfile(dataDir, sequence, 'test', 'test_imgs.txt'));
  valimgs = rfile(fullfile(dataDir, sequence, 'test', 'validation_imgs.txt'));
  allimgs = [valimgs, testimgs];
  istest = [false(1, numel(valimgs)), true(1, numel(valimgs))];
  [allimgs_u, ui, ic] = unique(allimgs);
  istest = istest(ui);
  for imi_l = 1:numel(allimgs_u)
    [~, filename, ext] = fileparts(allimgs_u{imi_l});
    imPath = getImPath(sequence, [filename, ext]);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi} = struct('id', imi, ...
      'name', sprintf('%s-%s', sequence, filename), 'path', imPath, ...
      'sequence', sequence, 'istest', istest(imi_l), 'isval', ~istest(imi_l), ...
      'imsize', utls.get_image_size(imPath));
    imi = imi + 1;
  end
  pidx = numel(allimgs)/2;
  for pi = 1:pidx
    ima = imdb.images{ic(pi) + lastim}; imb = imdb.images{ic(pi+pidx) + lastim};
    assert(strcmp(ima.sequence, imb.sequence));
    imdb.tasks{end+1} = struct(...
      'ima', ima.name, 'imb', imb.name, ...
      'ima_id', refim, 'imb_id', imi, 'H', eye(3), ...
      'ima_size', ima.imsize, 'imb_size', imb.imsize, ...
      'istest', ima.istest, 'isval', imb.isval, 'sequence', sequence, ...
      'description', struct('impair', [pi, pi+pidx]));
  end
  lastim = imi - 1; 
end

imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'webcam';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.geometry = 'homography';
imdb.rootdir = opts.rootDir;

end


