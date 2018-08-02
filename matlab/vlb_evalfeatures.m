function [scores, info] = vlb_evalfeatures( benchFun, imdb, feats, varargin )
%VLB_EVALFEATURES Run local features evaluation
%   VLB_EVALFEATURES benchfun imdb feats

% Copyright (C) 2017 Karel Lenc
% All rights reserved.
%
% This file is part of the VLFeat library and is made available under
% the terms of the BSD license (see the COPYING file).
opts.override = false;
opts.loadOnly = false;

imdb = dset.factory(imdb);
if isstruct(feats)
  featsname = feats.name;
  % Allow a feats configuration to set the override parameter
  if isfield(feats, 'override')
    opts.override = feats.override;
  end
else
  featsname = feats;
end

allargs = varargin;
opts.benchName = strrep(func2str(benchFun), 'bench.', '');
opts.taskids = 1:numel(imdb.tasks);
[opts, varargin] = vl_argparse(opts, varargin);

scoresdir = vlb_path('scores', imdb, featsname, opts.benchName);
vl_xmkdir(scoresdir);
scores_path = fullfile(scoresdir, 'results.csv');
info_path = fullfile(scoresdir, 'results.mat');
res_exists = exist(scores_path, 'file');
if nargout > 1
  res_exists = res_exists && exist(info_path, 'file');
end
if ~opts.override && res_exists
  scores = readtable(scores_path, 'delimiter', ',');
  if nargout > 1, info = load(info_path); end
  fprintf('Results loaded from %s.\n', scores_path);
  return;
end
if opts.loadOnly
  warning('Results %s not found.', scores_path);
  scores = table(); info = struct(); return;
end

fprintf('Running %d tasks of %s on %s for %s features.\n', ...
  numel(opts.taskids), opts.benchName, imdb.name, featsname);
status = utls.textprogressbar(numel(imdb.tasks), 'updatestep', 1);
scores = cell(1, numel(opts.taskids)); info = cell(1, numel(opts.taskids));
for ti = 1:numel(opts.taskids)
  task = imdb.tasks(opts.taskids(ti));
  fa = getfeats(imdb, featsname, task.ima);
  fb = getfeats(imdb, featsname, task.imb);
  matchGeom = imdb.matchFramesFun(task); % Returns a functor
  [scores{ti}, info{ti}] = benchFun(matchGeom, fa, fb, varargin{:});
  scores{ti}.benchmark = opts.benchName;
  scores{ti}.features = featsname;
  scores{ti}.dataset = imdb.name;
  scores{ti}.sequence = task.sequence;
  scores{ti}.ima = task.ima;
  scores{ti}.imb = task.imb;
  info{ti}.args = {allargs};
  status(ti);
end

scores = struct2table(cell2mat(scores), 'AsArray', true);
try
  writetable(scores, scores_path);
  info = cell2mat(info);
  save(info_path, 'info');
catch e
  fprintf('Cleaning up %s due to error', e.message);
  if exist(scores_path, 'file'), delete(scores_path); end
  if exist(info_path, 'file'), delete(info_path); end
  throw(e);
end

end

function feats = getfeats(imdb, featsname, imname)
featsdir = vlb_path('features', imdb, struct('name', featsname));
if ~isdir(featsdir)
    utls.features_not_found(featsdir);
end
featpath = fullfile(featsdir, imname);
feats = utls.features_load(featpath);
if isempty(feats)
  error('Unalbe to find %s features for image %s.', featsname, imname);
end
end
