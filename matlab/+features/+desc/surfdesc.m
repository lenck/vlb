function [ res ] = surfdesc( img, feats, varargin )

res.descName = 'surfdesc'; res.describes = 'frames';
if isempty(img) || isempty(feats.frames)
  res.descs = []; res.frames = zeros(3, 0);
  return;
end;

res = vl_override(res, features.utls.surf(img, feats, varargin{:}));

end


