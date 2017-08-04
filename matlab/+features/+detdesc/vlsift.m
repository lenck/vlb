function [ frames, descriptors, info ] = vlsift( img, varargin )

info.name = sprintf('vlsift-detdesc');

if isempty(img), frames = zeros(4, 0); descriptors = []; return; end;
img = utls.covdet_preprocessim(img);

[frames, descriptors] = vl_sift(img, varargin{:});

end

