function [ imdb ] = hsequences( varargin )

% Copyright (C) 2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

IMEXT = 'ppm';
NUMIMSEQ = 6;
DATADIR = 'hpatches-sequences-release';
NUMSEQUENCES = 116;

opts.url = 'http://www.iis.ee.ic.ac.uk/~vbalnt/hpatches/hpatches-sequences-release.tar.gz';
opts.rootDir = fullfile(vlb_path(), 'data', 'dataset-hsequences');
opts.matchFramesFun = @(g) ...
  @(fa, fb, varargin) geom.ellipse_overlap_H(g, fa, fb, ...
  'maxOverlapError', 0.5, varargin{:});
opts = vl_argparse(opts, varargin);

utls.provision(opts.url, opts.rootDir);

dataDir = fullfile(opts.rootDir, DATADIR);
getImPath = @(seq, imid) fullfile(dataDir, seq, sprintf('%d.%s', imid, IMEXT));
sequences = sort(utls.listdirs(dataDir));
assert(numel(sequences) == NUMSEQUENCES, 'Invalid number of sequences found.');

numImages = NUMIMSEQ*numel(sequences);
imdb.images = cell(1, numImages);
imdb.tasks = {};

imi = 1;
for sIdx = 1:numel(sequences)
  sequence = sequences{sIdx};
  refim = imi;
  if strcmp(sequence(1), 'i')
    category = 'illumination';
  elseif strcmp(sequence(1), 'v')
    category = 'viewpoint';
  else
    error('Invalid category');
  end
  for imi_l = 1:NUMIMSEQ
    imPath = getImPath(sequence, imi_l);
    assert(exist(imPath, 'file') == 2, 'Image %s not found.', imPath);
    imdb.images{imi}.id = imi;
    imdb.images{imi}.name = sprintf('%s-%d', sequence, imi_l);
    imdb.images{imi}.path = imPath;
    imdb.images{imi}.seqnum = imi_l;
    imdb.images{imi}.sequence = sequence;
    imdb.images{imi}.category = category;
    if imi_l == 1
      refImSize = utls.get_image_size(imPath);
      imi = imi + 1;
      continue;
    end;
    imSize =  utls.get_image_size(imPath);
    tfs = utls.read_vgg_homography(fullfile(dataDir, sequence, sprintf('H_1_%d', imi_l)));
    imdb.tasks{end+1} = struct('ima', imdb.images{refim}.name, ...
      'imb', imdb.images{imi}.name, 'H', tfs, ...
      'ima_size', refImSize, 'imb_size', imSize, ...
      'description', struct('sequence', sequence, 'category', category, ...
      'impair', [1, imi_l]));
    imi = imi + 1;
  end
end

imdb.images = cell2mat(imdb.images);
imdb.tasks = cell2mat(imdb.tasks);
imdb.name = 'hpatches-sequences';
imdb.matchFramesFun = opts.matchFramesFun;
imdb.geometry = 'homography';
imdb.rootdir = opts.rootDir;

end


