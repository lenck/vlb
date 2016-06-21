function [ precision, recall, info ] = vlb_desc_benchmark( matchFrames, ...
  fa, da, fb, db, varargin )
% VLB_DESC_BENCHMARK Descriptors matching PR curves
%
% Options:
%
%   OverlapError:: 0.5
%     Maximal overlap error of two frames to be considered as a valid
%     correspondence.
%
%   CropFrames:: true
%     Crop the frames out of overlapping regions (regions present in both
%     images).
%
%   WarpMethod:: 'linearise'
%     Numerical method used for warping ellipses. Available mathods are
%     'standard' and 'linearise' for precise reproduction of IJCV2005
%     benchmark results.
%
%   DescriptorsDistanceMetric:: 'L2'
%     Distance metric used for matching the descriptors. See
%     documentation of vl_alldist2 for details.
%
%   See also: datasets.VggAffineDataset, vl_alldist2
%
%   REFERENCES
%   [1] K. Mikolajczyk, C. Schmid. A performace Evaluation of Local
%       Descriptors. IEEE PAM, 2005.

opts.matchingStrategy = 'threshold';
opts.metric = 'L2';
opts.numPrPoints = inf;
opts = vl_argparse(opts, varargin);

MATCH_STRATEGIES = {'threshold', 'nn', 'nndistratio'};
assert(ismember(opts.matchingStrategy, MATCH_STRATEGIES), ...
  'Invalid matching strategy.');

info = struct(); precision = []; recall = [];
if isempty(fa) || isempty(fb), return; end
if size(fa,2) ~= size(da,2) || size(fb,2) ~= size(db,2)
  error('Number of frames and descriptors must be the same.');
end

[tcorr, corr_score, info] = matchFrames(fa, fb);
if isempty(tcorr), return; end;
da = da(:, info.fa_valid); db = db(:, info.fb_valid);

fa_num = size(da, 2); fb_num = size(db, 2);
% Create indexes of positive values in incidence matrix
tcorrIdxs = sub2ind([fa_num, fb_num], tcorr(1, :), tcorr(2, :));

switch opts.matchingStrategy
  case 'threshold'
    % Count number of correspondences for each frame
    nc = size(corr_score, 2);
  case {'nn','nndistratio'}
    % Sort the edges by decrasing score
    [~, perm] = sort(corr_score, 'descend');
    tcorr_s = tcorr(:, perm);
    % Find one to one stable matching
    geometryMatches = vlb_greedy_matching(fa_num, fb_num, tcorr_s(1:2,:)');
    geometryMatches = geometryMatches(1, :);
    info.geometryMatches = geometryMatches;
    nc = sum(geometryMatches ~= 0);
end

score = []; matches = []; labels = [];
switch opts.matchingStrategy
  case 'threshold'
    [matches, dists] = utls.alldist_edges(da, db, 'metric', opts.metric);
    [dists, perm] = sort(dists(:), 'ascend');
    labels = -ones(fa_num, fb_num);
    labels(tcorrIdxs) = 1;
    labels = labels(perm);
    score = -dists(:);
    labels = labels(:);
  case {'nn','nndistratio'}
    switch opts.matchingStrategy
      case 'nn'
        [matches, dists] = utls.match_greedy(db, da, 'metric', opts.metric);
      case 'nndistratio'
        [matches, dists] = utls.match_greedy_2nn(db, da, 'metric', opts.metric);
    end
    score = -inf(1,fa_num);
    labels = -ones(1,fa_num);
    % In case of nn, dists contains descriptor distance -> use
    % inverse. In case of second closes it contains ratio of the
    % closest to the second closest - use inverse as well.
    % In original KM code the second closest ratio is a ratio of the
    % second closest to the closest descriptor (inverse).
    score(matches(2,:)) = -dists;
    % Idxs of matches in incidence matrix
    matchesIdxs = sub2ind([fa_num, fb_num], matches(2,:), matches(1,:));
    % Find matches with enough overlap
    [~, validMatch] = intersect(matchesIdxs, tcorrIdxs);
    labels(matches(2,validMatch)) = 1;
end
numCorrectMatches = sum(labels > 0);
[recall, precision, info_pr] = vl_pr(labels, score, 'NumPositives', nc);
info = vl_override(info, info_pr);
info.numCorresp = nc;
info.numCorrectMatches = numCorrectMatches;
info.descMatches = matches;
info.descDists = dists;

if ~isinf(opts.numPrPoints)
  numValues = numel(recall);
  switch opts.matchingStrategy
    case 'threshold'
      samples = round(logspace(0,log10(numValues), opts.prPointsNum));
    case {'nn','nndistratio'}
      samples = round(linspace(1, numValues, opts.prPointsNum));
  end
  info.recall_all = recall;
  info.precision_all = precision;
  recall = recall(samples);
  precision = precision(samples);
end
info.matches = matches; info.labels = labels; info.distances = dists;

