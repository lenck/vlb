function [x, info] = meanstd(patches)
info = struct('name', mfilename, 'describes', 'patches');
if isempty(patches), x = []; return; end;

patches = single(squeeze(patches));
meanVal = reshape(mean(mean(patches, 1), 2), 1, []);
patchSz = [size(patches, 1), size(patches, 2)];
stdVal = std(reshape(single(patches), prod(patchSz(:)), []), 0, 1);
x = [meanVal; stdVal];

end