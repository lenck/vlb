function patches_save(patches, respath, scalingFactor)
assert(size(patches, 3) == 1 || size(patches, 3) == 3, ...
  'Patches has to be stored along 4th dimension.');
patchim = vl_imarray(squeeze(patches), 'Layout', [size(patches, 4), 1]);
[~,~,ext] = fileparts(respath);
assert(ismember(ext, {'.png', '.jpeg', '.jpg'}));
try
  imwrite(patchim, respath, 'Comment', sprintf('ScalingFactor:%.6f', scalingFactor));
catch e
  fprintf('Cleaning up %s due to error', respath);
  if exist(respath, 'file'), delete(respath); end
  throw(e);
end
end