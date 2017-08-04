function [ frames, info ] = vlsift( img, varargin )

info.name = sprintf('vlsift');

if isempty(img), frames = zeros(4, 0); return; end;
img = utls.covdet_preprocessim(img);

frames = vl_sift(img, varargin{:});

end

