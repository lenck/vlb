function res = ddet(img, varargin)

opts.url = 'https://codeload.github.com/lenck/ddet/zip/master';
opts.rootDir = fullfile(vlb_path(), 'data', 'ddet');
[opts, varargin] = vl_argparse(opts, varargin);
opts.binDir = fullfile(opts.rootDir, 'ddet-master');
opts.netsDir = fullfile(opts.binDir, 'nets');
opts.netsUrl = fullfile(opts.binDir, 'nets', 'nets.url');
[opts, varargin] = vl_argparse(opts, varargin);
opts.net = fullfile(opts.netsDir, 'detnet_s2.mat');
opts.thr = 4;
opts = vl_argparse(opts, varargin);

[~,netname,~] = fileparts(opts.net);
res.detName = sprintf('ddet-%s', netname); res.args = opts;
if isempty(img), res.frames = zeros(5, 0); return; end;

utls.setup_matconvnet();
utls.provision(opts.url, opts.rootDir, 'forceExt', '.zip');
utls.provision(opts.netsUrl, opts.netsDir);
if ~exist('DDet.m', 'file')
  addpath(opts.binDir);
  vlb_setup();
  delete(fullfile(opts.binDir, '+utls', 'provision.m'));
end
net = dagnn.DagNN.loadobj(load(opts.net));
det = DDet(net, 'thr', opts.thr);

[frames, ~, info] = det.detect(img);
res.frames = frames;
res.peakScores = info.peakScores;

end