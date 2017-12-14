function res = tilde(img, varargin)

opts.url = 'https://github.com/cvlab-epfl/TILDE/archive/master.zip';
opts.rootDir = fullfile(vlb_path('vendor'), 'tilde');
[opts, varargin] = vl_argparse(opts, varargin);
opts.srcDir = fullfile(opts.rootDir, 'TILDE-master', 'matlab', 'src');
opts.filtersDir = fullfile(opts.rootDir, 'TILDE-master', 'matlab', 'filters');
[opts, varargin] = vl_argparse(opts, varargin);
opts.fullPathFilter = fullfile(opts.filtersDir, 'BestFilters_2percents/Original/MexicoMed.mat');
opts.fixed_scale = 10;
opts = vl_argparse(opts, varargin);

global sRoot;
global bSetupPathFin;
res.detName = 'tilde'; res.args = opts; res.frames = zeros(5, 0);
if isempty(img), return; end

imsz = [size(img, 1), size(img, 2)];
if any(imsz < 105)
  padding = ceil(max(105 - imsz, 0) ./ 2);
  img = padarray(img, [padding, 0], 'replicate');
end

utls.provision(opts.url, opts.rootDir, 'forceExt', '.zip');

if ~exist('ApplyLearnedELLFilter', 'file')
  addpath(fullfile(opts.srcDir, 'Utils'));
  addpath(fullfile(opts.srcDir, 'Utils/tools_nonmax/'));
  addpath(fullfile(opts.srcDir, 'Utils/tools_evaluate/'));
  addpath(fullfile(opts.srcDir, 'Utils/tools_filtering/'));
  addpath(fullfile(opts.srcDir, '../external/dollarToolbox/'));
  
  sRoot = fileparts(opts.srcDir);
  setup_path;
end

stime = tic;
[ binary_res, score ] = ApplyLearnedELLFilter(img, -inf, opts.fullPathFilter, false );
idx = find(binary_res);
[I, J] = ind2sub(size(binary_res), idx);
features = [J I zeros(size(I,1),3) repmat(opts.fixed_scale, size(I,1), 1)]';
features = mergeScoreImg2Keypoints(features, score);
res.dettime = stime;

res.detresponses = features(5, :);
res.frames = [features(1:2, :); features(end, :)];
end