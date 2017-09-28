function [scores, info] = detmatch(matchGeom, feats_a, feats_b, varargin)
% DETMATCH Compute matching score of given image features
%   [SCORES] = obj.testFeatures(TF, IMAGE_A_SIZE,
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
opts.matchGeometry = true;
opts.matchDescriptors = @utls.match_greedy; 
opts.geomMode = 'descriptors';
opts = vl_argparse(opts, varargin);

fa = feats_a.frames; fb = feats_b.frames;
da = feats_a.descs; db = feats_b.descs;

info = struct('geom', [], ); 
scores = struct('matchingScore', 0, 'numMatches', 0, ...
  'repeatability', 0, 'numCorresp', 0);

if isempty(fa) || isempty(fb), return; end;
if isempty(da) || isempty(db), return; end;
if size(fa, 2) ~= size(da, 2) || size(fb,2) ~= size(db,2)
  obj.error('Number of frames and descriptors must be the same.');
end

[scores, ri] = bench.detrep(matchGeom, feats_a, feats_b);
info.rep = ri;
if isempty(ri.matches), return; end
fa = fa(:, ri.geom.fa_valid); da = da(:, ri.geom.fa_valid);
fb = fb(:, ri.geom.fb_valid); db = db(:, ri.geom.fb_valid);

descMatchEdges = opts.matchDescriptors(db, da);
descMatches = zeros(1, size(fa, 2));
descMatches(descMatchEdges(2, :)) = descMatchEdges(1, :);
info.descMatches = descMatches;

if opts.matchGeometry
  % A match valid when 1-to-1 matched for both geom and desc
  matches = descMatches;
  matches(descMatches ~= ri.matches) = 0;
else
  % A match valid when among tentative correspondences which are expressed
  % as edges in the bipartite graph.
  fsz = [size(fa, 2), size(fb, 2)];
  tcorrIdxs = sub2ind(fsz, ri.tcorr(1,:), ri.tcorr(2,:));
  % descMatchEdges are B->A
  matchIdxs = sub2ind(fsz, descMatchEdges(2,:), descMatchEdges(1,:));
  [~, validMatch] = intersect(matchIdxs, tcorrIdxs);
  matches = zeros(1, size(descMatches, 2));
  matches(descMatchEdges(2, validMatch)) = descMatchEdges(1, validMatch);
end

info.matches = matches;
% Compute the score
nm = sum(matches ~= 0);
fa_num = sum(ri.fa_valid); fb_num = sum(ri.fb_valid);
switch opts.normFactor
  case 'minab'
    ms = nm / min(fa_num, fb_num);
  case 'a'
    ms = nm / fa_num;
  case 'b'
    ms = nm / fb_num;
  otherwise
    error('Invalid `normFactor`.');
end
scores.matchingScore = ms; scores.numMatches = nm;
scores.numCorresp = info.numCorresp;