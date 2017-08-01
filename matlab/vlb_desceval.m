function [scores, info] = vlb_desceval( imdb, detector, descriptor, varargin )


% Copyright (C) 2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).

opts.benchFun = @bench.descmatch_eval;
[opts, varargin] = vl_argparse(opts, varargin);
opts.benchName = strrep(func2str(opts.benchFun), 'bench.', '');
opts.override = false;
[opts, varargin] = vl_argparse(opts, varargin);

imdb = dset.dsetfactory(imdb);
detector = det.detfactory(detector, varargin{:});
descriptor = desc.descfactory(descriptor, varargin{:});

  function data = getfeats(type, imname)
    switch type
      case 'dets'
        path = fullfile(vlb_path(type, imdb, detector), [imname, '.csv']);
      case 'descs'
        path = fullfile(vlb_path(type, imdb, detector, descriptor), [imname, '.csv']);
    end
    if ~exist(path, 'file'), error('Unable to find %s.', path); end;
    data = dlmread(path, ';')';
  end

scoresdir = vlb_path('scores', struct('name', opts.benchName), ...
  imdb, detector, descriptor);
vl_xmkdir(scoresdir);
scores_path = fullfile(scoresdir, 'results.csv');
info_path = fullfile(scoresdir, 'results.mat');
if ~opts.override && exist(scores_path, 'file') && exist(info_path, 'file')
  scores = readtable(scores_path); info = load(info_path);
  fprintf('Results loaded from %s.\n', scores_path);
  return;
end;

fprintf('Running %d tasks of %s on %s for %s det. and %s desc.\n', ...
  numel(imdb.tasks), opts.benchName, imdb.name, detector.name, descriptor.name);
status = utls.textprogressbar(numel(imdb.tasks), 'updatestep', 1);
scores = cell(1, numel(imdb.tasks)); info = cell(1, numel(imdb.tasks));
for ti = 1:numel(imdb.tasks)
  task = imdb.tasks(ti);
  fa = getfeats('dets', task.ima); fb = getfeats('dets', task.imb);
  da = getfeats('descs', task.ima); db = getfeats('descs', task.imb);
  matchGeom = @(varargin) imdb.defGeom(task, varargin{:});
  [scores{ti}, info{ti}] = opts.benchFun(matchGeom, fa, da, fb, db, varargin{:});
  scores{ti}.dataset = imdb.name;
  scores{ti}.detector = detector.name; scores{ti}.descriptor = descriptor.name;
  scores{ti}.ima = task.ima; scores{ti}.ima = task.imb;
  status(ti);
end

scores = struct2table(cell2mat(scores), 'AsArray', true);
writetable(scores, scores_path);
info = cell2mat(info);
save(info_path, '-struct', 'info');

end

