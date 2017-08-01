function [results, info] = vgg_desc_benchmark(geom, ...
  ima_p, fa, da, imb_p, fb, db, varargin)
%VGG_DESC_BENCHMARK Summary of this function goes here
opts.maxOverlapError = 0.5;
opts = vl_argparse(opts, varargin);

BIN_URL = 'http://www.robots.ox.ac.uk/~vgg/research/affine/det_eval_files/repeatability.tar.gz';
BIN_DIR = fullfile(vlb_path(), 'data', 'km_frames_benchmark');
% Make sure all supplementary files are present
if ~exist(fullfile(BIN_DIR, 'repeatability.m'), 'file')
  untar(BIN_URL, BIN_DIR);
end
if ~exist(fullfile(BIN_DIR, ['descdist.', mexext]), 'file')
  mex(fullfile(BIN_DIR, 'descdist.cxx'), '-outdir', BIN_DIR);
end
if ~exist(fullfile(BIN_DIR, ['c_eoverlap.', mexext]), 'file')
  mex(fullfile(BIN_DIR, 'c_eoverlap.cxx'), '-outdir', BIN_DIR);
end
assert(size(fa, 2) == size(da, 2), 'Invalid number of frames/descriptors');
assert(size(fb, 2) == size(db, 2), 'Invalid number of frames/descriptors');

tmpFile = tempname;
ella_p = [tmpFile, 'ellA.txt']; ellb_p = [tmpFile, 'ellB.txt'];
ella_f = utls.frame2ellipse(fa); ellb_f = utls.frame2ellipse(fb);
legacy.vgg_features_write(ella_p, ella_f, da);
legacy.vgg_features_write(ellb_p, ellb_f, db);
tmpH_p = [tmpFile, 'H.txt']; H = geom.H; save(tmpH_p, 'H','-ASCII');
overlap_err_idx = round(opts.maxOverlapError*10);

addpath(BIN_DIR);
rehash;
[~, rep_sc_t, nc_t, ms, numMatches, twi] = ...
  repeatability(ella_p, ellb_p, tmpH_p, ima_p, imb_p, 0);
rep_sc = rep_sc_t(overlap_err_idx)./100;
nc = nc_t(overlap_err_idx);
ms = ms ./ 100;
[corrMatchNn, totMatchNn, corrMatchSim, totMatchSim, corrMatchRn, totMatchRn] = ...
  descperf(ella_p, ellb_p, tmpH_p, ima_p, imb_p, nc, twi);
rmpath(BIN_DIR);

delete(ella_p); delete(ellb_p); delete(tmpH_p);

results = struct();

results.threshold.recall = corrMatchSim / sum(twi(:));
results.threshold.precision = corrMatchSim ./ totMatchSim;

results.nn.recall = corrMatchNn / nc;
results.nn.precision = corrMatchNn ./ totMatchNn;

results.nndistratio.recall = corrMatchRn / nc;
results.nndistratio.precision = corrMatchRn ./ totMatchRn;

info = struct('repScore',rep_sc, 'numCorresp', nc, ...
  'numSimCorresp', sum(twi(:)), 'matchScore', ms, ...
  'numMatches', numMatches);
end

