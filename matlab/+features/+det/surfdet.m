function [ res ] = surfdet( img, varargin )

res.detName = 'surfdet';
if isempty(img), res.frames = zeros(3, 0); return; end;

feats = features.utls.surf(img, [], varargin{:});
res = vl_override(res, feats);

end


