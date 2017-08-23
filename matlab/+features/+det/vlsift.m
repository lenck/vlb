function [ res ] = vlsift( img, varargin )

res.detName = sprintf('vlsift');
if isempty(img), res.frames = zeros(4, 0); return; end;
img = utls.covdet_preprocessim(img);

[res.frames, res.descs] = vl_sift(img, varargin{:});
res.args = varargin;
end

