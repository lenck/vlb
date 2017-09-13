function [ res ] = vlcovdet( img, varargin )

opts.Method = 'Dog';
opts.Descriptor = 'SIFT';
opts.PatchRelativeExtent = 5;
[opts, varargin] = vl_argparse(opts, varargin);

res.detName = sprintf('vlcovdet-det-%s', opts.Method);
if isempty(img), res.frames = zeros(6, 0); return; end;
img = utls.covdet_preprocessim(img);

[res.frames, res.descs, info] = vl_covdet(img, ...
  'Descriptor', opts.Descriptor, ...
  'PatchRelativeExtent', opts.PatchRelativeExtent, ...
  'Method', opts.Method, varargin{:});
res.detresponses = info.peakScores;
res.scalingFactor = opts.PatchRelativeExtent;
res.args = [{'Method', opts.Method}, varargin];
end

