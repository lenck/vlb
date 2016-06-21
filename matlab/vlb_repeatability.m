function [ rep, nm, info ] = vlb_repeatability( matchFrames, fa, fb, varargin )
% VLB_REPEATABILITY Compute repeatability of given image features
%   [SCORE NUM_MATCHES] = VLB_REPEATABILITY(TF, IMAGE_A_SIZE,
%   IMAGE_B_SIZE, FRAMES_A, FRAMES_B, DESCS_A, DESCS_B) Compute
%   matching score SCORE between frames FRAMES_A and FRAMES_B
%   and their descriptors DESCS_A and DESCS_B which were
%   extracted from pair of images with sizes IMAGE_A_SIZE and
%   IMAGE_B_SIZE which geometry is related by homography TF.
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
opts = vl_argparse(opts, varargin);

rep = 0; nm = 0; info = struct('geomMatches', zeros(2, 0));
if isempty(fa) || isempty(fb), return; end
[tcorr, corr_score, info] = matchFrames(fa, fb);
fa_num = sum(info.fa_valid); fb_num = sum(info.fb_valid);
info.tcorr = tcorr; info.corr_score = corr_score;
info.geomMatches = zeros(2, 0);
if isempty(tcorr), return; end;

% Sort the edgest by decrasing score
[~, perm] = sort(corr_score, 'descend');
tcorr_s= tcorr(:, perm);
% Approximate the best bipartite matching
matches = vlb_greedy_matching(fa_num, fb_num, tcorr_s');
matches = matches(1, :);
info.geomMatches = matches;

% Compute the score
nm = sum(matches ~= 0);
switch opts.normFactor
  case 'minab'
    rep = nm / min(fa_num, fb_num);
  case 'a'
    rep = nm / fa_num;
  case 'b'
    rep = nm / fb_num;
  otherwise
    error('Invalid `normFactor`.');
end
