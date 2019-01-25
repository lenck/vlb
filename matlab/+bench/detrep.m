function [ scores, info ] = detrep( matchFrames, feats_a, feats_b, varargin )
% VLB_REPEATABILITY Compute repeatability of given image features
%   [SCORES] = VLB_REPEATABILITY(MATCH, FRAMES_A, FRAMES_B)
%   Computes the repeatability between frames FRAMES_A and FRAMES_B
%   NUM_MATHCES is number of matches which is calcuated
%   according to object settings.
%
%   [SCORE, NUM_MATCHES, REPR_FRAMES, MATCHES] =
%   obj.testFeatures(...) returns cell array REPR_FRAMES which
%   contains reprojected and eventually cropped frames in
%   format:
%
%   REPR_FRAMES = {CFRAMES_A,CFRAMES_B,REP_CFRAMES_A,REP_CFRAMES_B}
%
%   where CFRAMES_A are (cropped) frames detected in the IMAGEAPATH
%   image REP_CFRAMES_A are CFRAMES_A reprojected to the IMAGEBPATH
%   image using homography TF. Same hold for frames from the secons
%   image CFRAMES_B and REP_CFRAMES_B.
%   MATCHES is an array of size [size(CFRAMES_A),1]. Two frames are
%   CFRAMES_A(k) and CFRAMES_B(l) are matched when MATCHES(k) = l.
%   When frame CFRAMES_A(k) is not matched, MATCHES(k) = 0.

opts.normFactor = 'minab';
opts.topn = inf;
opts.forceTopn = true;
opts.magnifyFrames = [];
[opts, varargin] = vl_argparse(opts, varargin);

info.geom = []; 
info.tcorr = zeros(2, 0);  info.corr_score = zeros(1, 0);
info.geomMatches = zeros(2, 0); info.matches = zeros(1, 0); 
scores = struct('repeatability', 0, 'numCorresp', 0);
if isempty(feats_a.frames) || isempty(feats_b.frames), return; end
if ~isinf(opts.topn) && isfield(feats_a, 'detresponses') && ...
    isfield(feats_b, 'detresponses')
  feats_a = utls.topnframes(feats_a, opts.topn);
  feats_b = utls.topnframes(feats_b, opts.topn);
elseif ~isinf(opts.topn) && opts.forceTopn
  error('Features do not have `detresponses` fields for a topn.');
end
if ~isempty(opts.magnifyFrames)
  feats_a.frames = utls.frame_magnify_scale(feats_a.frames, opts.magnifyFrames);
  feats_b.frames = utls.frame_magnify_scale(feats_b.frames, opts.magnifyFrames);
end
feats_a.descs = []; feats_b.descs = [];
[tcorr, corr_score, info.geom] = matchFrames(feats_a.frames, feats_b.frames, varargin{:});
info.tcorr = tcorr;  info.corr_score = corr_score;
fa_num = sum(info.geom.fa_valid); fb_num = sum(info.geom.fb_valid);
if isempty(tcorr), return; end

% Sort the edgest by decrasing score
[~, perm] = sort(corr_score, 'descend');
tcorr_s= tcorr(:, perm);
% Approximate the best bipartite matching
matches = vlb_greedy_matching(fa_num, fb_num, tcorr_s');
matches = matches(1, :);
info.matches = matches;

% Compute the score
nc = sum(matches ~= 0);
switch opts.normFactor
  case 'minab'
    rep = nc / min(fa_num, fb_num);
  case 'a'
    rep = nc / fa_num;
  case 'b'
    rep = nc / fb_num;
  otherwise
    error('Invalid `normFactor`.');
end
scores = struct('repeatability', rep, 'numCorresp', nc);