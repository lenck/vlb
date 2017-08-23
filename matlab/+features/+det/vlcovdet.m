function [ res ] = vlcovdet( img, varargin )

opts.Method = 'Dog';
[opts, varargin] = vl_argparse(opts, varargin);
res.detName = sprintf('vlcovdet-det-%s', opts.Method);
if isempty(img), res.frames = zeros(6, 0); return; end;
img = utls.covdet_preprocessim(img);

[res.frames, res.descs, info] = vl_covdet(img, 'PatchRelativeExtent', 1, ...
  'Method', opts.Method, varargin{:});
res.detresponses = info.peakScores;
res.args = [{'Method', opts.Method}, varargin];
end

