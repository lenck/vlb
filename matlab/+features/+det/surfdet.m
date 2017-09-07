function [ res ] = surfdet( img, varargin )

res.detName = 'surfdet';
if isempty(img), res.frames = zeros(3, 0); return; end;

res = vl_override(res, features.utls.surf(img, [], varargin{:}));

end


