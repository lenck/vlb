function [ res ] = vlsift( img, varargin )
opts.Magnif = 5;
[opts, varargin] = vl_argparse(opts, varargin);

res.detName = sprintf('vlsift');
if isempty(img), res.frames = zeros(4, 0); return; end;
img = utls.covdet_preprocessim(img);

[res.frames, res.descs] = vl_sift(img, 'Magnif', opts.Magnif, varargin{:});
res.scalingFactor = opts.Magnif;
res.args = varargin;

end

