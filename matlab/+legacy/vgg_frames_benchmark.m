function [ repScore, numCorresp, matchScore, numMatches ] = ...
  vgg_frames_benchmark( geom, ima_p, fa, da, imb_p, fb, db, varargin)
% VGG_FRAMES_BENCHMARK Compute scores of image features
%   [REP, NUM_CORR, MATCHING, NUM_MATCHES] = VGG_FRAMES_BENCHMARK(GEOM,
%   IMAGEA_PATH, FRAMES_A, DESCRIPTORS_A, IMAGEB_PATH, FRAMES_B,
%   DESCRIPTORS_B) Compute repeatability REP and matching MATHICNG score
%   between FRAMES_A and FRAMES_B which are related by homography TF and
%   their descriptors DESCRIPTORS_A and DESCRIPTORS_B which were
%   extracted from images IMAGE_A and IMAGE_B.
%
%   [REP, NUM_CORR] = obj.testFeatures(TF, IMAGEA_PATH, FRAMES_A, [],
%   IMAGEB_PATH, FRAMES_B, []) Compute only repeatability
%   between the the frames FRAMES_A and FRAMES_B.

opts.maxOverlapError = 0.4;
opts.commonPart = 1;
opts = vl_argparse(opts, varargin);

% Constants
BIN_URL = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/repeatability.tar.gz';
BIN_DIR = fullfile(vlb_root(), 'data', 'km_frames_benchmark');
% Make sure all supplementary files are present
if ~exist(fullfile(BIN_DIR, 'repeatability.m'), 'file')
  untar(BIN_URL, BIN_DIR);
end
if exist(fullfile(BIN_DIR, ['c_eoverlap', mexext]), 'file')
  vlb_compile();
  copyfile(...
    fullfile(vlb_root(), 'matlab', 'mex', ['vgg_compute_ellipse_overlap.', mexext]), ...
    fullfile(BIN_DIR, ['c_eoverlap.', mexext]));
end

if ~isempty(da)
  assert(size(fa, 2) == size(da, 2), 'Invalid number of frames/descriptors');
end
if ~isempty(db)
  assert(size(fb, 2) == size(db, 2), 'Invalid number of frames/descriptors');
end

tmpFile = tempname;
ellb_p = [tmpFile 'ellB.txt']; ella_p = [tmpFile 'ellA.txt'];
ella_f = utls.frame_to_ellipse(fa); ellb_f = utls.frame_to_ellipse(fb);
legacy.vgg_features_write(ella_p, ella_f, da);
legacy.vgg_features_write(ellb_p, ellb_f, db);
tmpH_p = [tmpFile 'H.txt']; H = geom.H; save(tmpH_p, 'H', '-ASCII');
overlap_err_idx = round(opts.maxOverlapError*10);

addpath(BIN_DIR);
rehash;
[~, tmprepScore, tmpnumCorresp, matchScore, numMatches, ~] = repeatability(...
  ella_p, ellb_p, tmpH_p, ima_p, imb_p, opts.commonPart);
rmpath(BIN_DIR);

repScore = tmprepScore(overlap_err_idx)./100;
numCorresp = tmpnumCorresp(overlap_err_idx);
matchScore = matchScore ./ 100;
delete(ella_p);
delete(ellb_p);
delete(tmpH_p);
